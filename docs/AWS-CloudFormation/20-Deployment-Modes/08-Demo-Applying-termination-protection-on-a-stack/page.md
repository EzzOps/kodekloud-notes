# Demo Applying termination protection on a stack

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Deployment-Modes/Demo-Applying-termination-protection-on-a-stack/page

Guide to enabling and disabling AWS CloudFormation termination protection to prevent accidental stack deletion and explain deletion behavior.

In this short demo we'll enable termination protection on an AWS CloudFormation stack so it cannot be deleted accidentally. The example uses a simple S3-backed template created from the CloudFormation console.

Follow these steps to create the stack and enable termination protection.

1. Create the stack
   * In the CloudFormation console choose Create stack and upload your template (for example, a basic S3 template).
   * Click Next, enter a stack name, continue through the wizard, and create the stack.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Specify stack details&#x22; step, showing the &#x22;Stack name&#x22; field filled with &#x22;DemoStack&#x22; and an open suggestion list of other stack names. The left sidebar shows the multi-step wizard (Create stack → Specify stack details → Configure stack options → Review and create)." />
</Frame>

2. Wait for the stack to reach CREATE\_COMPLETE
   * After the stack reaches CREATE\_COMPLETE (or any active state), select it in the Stacks list.
   * From the “Stack actions” menu choose **Edit termination protection** to change the setting.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Stacks&#x22; console showing one stack named &#x22;DemoStack&#x22; with status CREATE_COMPLETE and its created time. The &#x22;Stack actions&#x22; dropdown is open, listing options like &#x22;Edit termination protection,&#x22; &#x22;View drift results,&#x22; and &#x22;Detect drift.&#x22;" />
</Frame>

> **lightbulb** Termination protection prevents deletion of the entire CloudFormation stack through CloudFormation until you explicitly disable it. It does not block stack updates, nor does it stop direct modifications to individual resources made outside CloudFormation (those actions can still cause drift).

3. What happens when you try to delete a protected stack
   * If termination protection is enabled and you attempt to delete the stack, the console prevents the deletion and asks you to disable termination protection first.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing a &#x22;Delete stack?&#x22; dialog that warns termination protection is enabled and prompts you to disable it first. The background shows a stack named &#x22;DemoStack&#x22; and an orange &#x22;Edit termination protection&#x22; button." />
</Frame>

> **warning** To delete a protected stack you must first turn off termination protection and save the change. Deleting without disabling termination protection via CloudFormation is blocked by the service.

4. Disable termination protection (if you want to delete)
   * Re-open **Stack actions → Edit termination protection**, set the option to **Deactivated**, and click Save.
   * After saving, refresh the stack list — you will be able to delete the stack normally.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing a dialog titled &#x22;Edit termination protection for DemoStack?&#x22; with radio options for Deactivated (selected) and Activated. The modal explains termination protection prevents accidental deletion and the Save button is being clicked." />
</Frame>

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Stacks&#x22; console with a green success banner saying termination protection was changed. The page shows one stack named &#x22;DemoStack&#x22; with status CREATE_COMPLETE and its creation timestamp." />
</Frame>

Quick reference

| Action                         | Console path                                                     | CLI / API                                                                                    |
| ------------------------------ | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Enable termination protection  | Stack actions → Edit termination protection → Activated → Save   | Use the UpdateTerminationProtection API. See AWS docs for the exact CLI parameters.          |
| Disable termination protection | Stack actions → Edit termination protection → Deactivated → Save | Use the UpdateTerminationProtection API (set EnableTerminationProtection to false).          |
| Delete stack                   | Stacks list → Select stack → Delete                              | Stack deletion is blocked while termination protection is enabled. Disable protection first. |

Further reading

* [AWS CloudFormation — Stack deletion and termination protection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-delete.html)
* [AWS CloudFormation API: UpdateTerminationProtection](https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_UpdateTerminationProtection.html)

Summary

* Enable termination protection from Stack actions → Edit termination protection to guard against accidental stack deletion.
* To delete a stack, you must first deactivate termination protection and save the change.
* Termination protection prevents deletion via CloudFormation; it does not block updates or direct modifications to resources outside CloudFormation.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/68ab5c12-a35c-46b7-aef2-2e274c10989c/lesson/4fada431-5b99-4296-b5e2-4cf631bee7fd)
