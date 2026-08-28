# Example matrix A (3x3)
A = np.array([
    [1.0, 4.0, 7.0],
    [1.0, 5.0, 8.0],
    [1.0, 6.0, 10.5]
])

# Compute full SVD
U_full, S_full, Vt_full = np.linalg.svd(A, full_matrices=False)

# Choose rank k = 2 for approximation
k = 2
U_k = U_full[:, :k]
S_k = np.diag(S_full[:k])
Vt_k = Vt_full[:k, :]

# Reconstruct rank-k approximation
A_k = U_k @ S_k @ Vt_k

print("Original A:\n", A)
print("\nRank-{} approximation A_k:\n".format(k), A_k)
```

The truncated singular values indicate component importance; small singular values can often be discarded with limited downstream impact.

Recap: technique trade-offs

|              Technique |           What it reduces | Pros                                                                      | Cons / Considerations                                                 |
| ---------------------: | ------------------------: | ------------------------------------------------------------------------- | --------------------------------------------------------------------- |
|                Pruning |      Parameters & compute | Can give large size reductions; structured variants are hardware-friendly | Often requires iterative retraining and careful sparsity patterns     |
|           Quantization |       Precision & storage | Major size and latency wins on supported hardware                         | Possible accuracy loss; needs calibration or QAT                      |
|           Distillation |            Model capacity | Produces small, high-quality student models                               | Requires additional training and dataset passes                       |
| Low-rank factorization | Matrix size & computation | Reduces FLOPs for dense layers; mathematically principled                 | Rank selection affects accuracy; not always best for attention layers |

Choosing the right combination depends on model architecture, deployment hardware, and acceptable accuracy trade-offs. In practice, teams combine techniques—e.g., distill a student model, then quantize it and apply light pruning.

<Frame>
  <img alt="The image illustrates the workflow of Amazon SageMaker Neo, showing the process from creating a model with Amazon SageMaker, through compilation jobs, to deploying a compiled model to Amazon S3 and an edge device." />
</Frame>

SageMaker Neo (concept)
A trained model from Amazon SageMaker can be sent to a compilation job where SageMaker Neo produces a hardware-optimized compiled model. The optimized artifact can be stored in Amazon S3 and deployed to edge devices or specific environments. This workflow enables the same model logic to run faster with lower latency on target hardware without manual low-level optimizations.

* SageMaker Neo docs: [https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-neo.html](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-neo.html)
* Amazon SageMaker: [https://aws.amazon.com/sagemaker/](https://aws.amazon.com/sagemaker/)
* Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)

Best practices

1. Understand trade-offs — measure compression impact on accuracy, latency, and memory. Prioritize metrics that matter for your product (e.g., 95th percentile latency vs. mean latency).
2. Match technique to hardware — structured pruning and INT8 quantization are often better supported on edge CPU/GPU/ISP stacks.
3. Iterate and tune — sweep pruning rates, quantization schemes, distillation temperatures, and rank k values to find the best balance.
4. Profile on target device — benchmarks on simulators or desktops can differ from real hardware due to memory hierarchy and instruction set differences.
5. Regularize during training — weight decay, dropout, and early stopping improve robustness to compression.
6. Combine methods carefully — distill first, then quantize and prune lightly; verify end-to-end accuracy and latency.

<Callout icon="lightbulb">
  When evaluating compressed models, always benchmark real-world inference latency and accuracy on the target device. Simulator or desktop measurements can differ from on-device behavior.
</Callout>

<Callout icon="warning">
  Beware: aggressive compression (very low rank, extreme pruning, or INT8 quantization without calibration) can cause unacceptable accuracy degradation. Validate thoroughly and keep rollback plans for production deployments.
</Callout>

Links and references

* [NumPy SVD documentation](https://numpy.[AWS_SECRET_ACCESS_KEY].linalg.svd.html)
* [SageMaker Neo documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-neo.html)
* [Kubernetes Documentation (for deploying model servers)](https://kubernetes.io/docs/)
* [Edge AI and On-Device ML resources](https://www.tensorflow.org/lite)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/f3f28bdc-5ae5-43bb-85b6-01f7b1bfb71b/lesson/d6ab35d9-7f01-4c9a-928c-bcb8a7eb97f7" />
</CardGroup>


# Regularization Techniques in ML

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Regularization-Techniques-in-ML/page

Overview of regularization methods to reduce overfitting and improve generalization in machine learning, covering L1 L2 Elastic Net dropout early stopping and SageMaker usage.

Underfitting happens when a model is too simple to capture the underlying patterns in the data, producing poor performance on both training and test sets. Overfitting occurs when a model learns the training data — including noise and outliers — so well that it fails to generalize to unseen data. The goal of regularization is to find a balanced model that generalizes well: not too simple (underfitting) and not overly complex (overfitting).

<Frame>
  <img alt="The image illustrates three graphs showing examples of underfitting, balanced fitting, and overfitting in data modeling. Each graph depicts a different type of line fitting a set of white data points." />
</Frame>

Regularization is a group of techniques that discourage overly complex models by adding a complexity penalty to the loss function. This penalty nudges model parameters toward smaller values or sparsity, improving generalization on unseen data.

<Frame>
  <img alt="The image illustrates the concept of regularization in machine learning, showing a model that overfits on a training dataset leading to high in-sample accuracy but low accuracy on new data, suggesting poor generalization." />
</Frame>

How regularization modifies the loss function:

* Base loss: measures prediction error (e.g., MSE, cross-entropy).
* Regularized loss: base loss + penalty term that grows with model complexity.
* Strength: controlled by a hyperparameter (commonly λ or `alpha`) that scales the penalty.

<Frame>
  <img alt="The image explains how regularization modifies the loss function by adding a penalty term to the error, involving a regularization strength hyperparameter (λ) and weight penalty." />
</Frame>

Common penalty functions and when to use them:

| Regularization | Penalty (concept)        | Effect                                                 | Use case                                 |
| -------------: | ------------------------ | ------------------------------------------------------ | ---------------------------------------- |
|     L1 (Lasso) | Sum of absolute weights  | Encourages sparsity (drives some coefficients to zero) | Feature selection, high-dimensional data |
|     L2 (Ridge) | Sum of squared weights   | Shrinks weights smoothly (reduces variance)            | When many small features contribute      |
|    Elastic Net | Combination of L1 and L2 | Balances sparsity and stability                        | When correlated features exist           |

<Frame>
  <img alt="The image depicts three types of regularization in machine learning: L1 (Lasso), L2 (Ridge), and Elastic Net, explaining their penalty calculations." />
</Frame>

Scikit-learn examples: Ridge (L2) and Lasso (L1)

```python theme={null}
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
