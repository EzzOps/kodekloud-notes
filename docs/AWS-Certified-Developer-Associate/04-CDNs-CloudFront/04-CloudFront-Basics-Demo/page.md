# CloudFront Basics Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/CDNs-CloudFront/CloudFront-Basics-Demo/page

This article explains how to configure AWS CloudFront to accelerate delivery of a web application using an S3 bucket.

In this article, we'll walk through configuring AWS CloudFront to accelerate delivery of a simple web application. The application consists of an HTML file, a CSS file, and several images stored in an S3 bucket. CloudFront caches these files at edge locations, enhancing load times across the globe.

## Step 1: Setting Up the S3 Bucket

Begin by creating an S3 bucket to host your web application files.

1. In the AWS S3 console, click on **Create bucket**.
2. Name your bucket (e.g., "kodekloud-cloudfront-demo") and leave the default settings unchanged.

<Frame>
  ![The image shows the AWS S3 interface for creating a new bucket, with options for general configuration, bucket type, and object ownership settings. The bucket name "kodekloud-cloudfront-demo" is being entered.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858469/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-s3-create-bucket-interface.jpg)
</Frame>

Once created, your new bucket will appear in the bucket list.

<Frame>
  ![The image shows an AWS S3 management console with a list of general-purpose buckets, including details like bucket names, AWS regions, and creation dates. A green notification bar at the top indicates the successful creation of a bucket named "kodekloud-cloudfront-demo."](../../../../images/kodekloud.com/kk-media/image/upload/v1752858471/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-s3-management-console-buckets.jpg)
</Frame>

Upload all your web application files—including the HTML file, CSS file, and images—to this bucket.

### Verifying File Access

Trying to access one of the files via its public URL will result in an "Access Denied" error because no public access policies are configured. Inspecting the bucket’s permissions confirms that there is no bucket policy enabled, thereby blocking public access.

<Frame>
  ![The image shows an Amazon S3 console displaying details of an object named "index.html" in a bucket, including its properties, S3 URI, and object URL.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858472/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/amazon-s3-index-html-details.jpg)
</Frame>

<Frame>
  ![The image shows an AWS S3 bucket permissions settings page, highlighting options for blocking public access and bucket policy configurations.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858473/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-s3-bucket-permissions-settings.jpg)
</Frame>

<Callout icon="lightbulb">
  Since CloudFront will act as the access point for your content, you can keep the S3 bucket secured and configure CloudFront to retrieve the files on your behalf.
</Callout>

## Step 2: Creating a CloudFront Distribution

Now, set up a CloudFront distribution to serve your S3 content:

1. Open the CloudFront console and click **Create Distribution**.
2. Choose the S3 bucket ("kodekloud-cloudfront-demo") as the origin.
3. Optionally, specify an origin path; if not needed, leave it as default.
4. You may provide a custom origin name or use the default one.
5. Under **Cache Behavior**, retain the default settings, and scroll down to view additional configuration options.

<Frame>
  ![The image shows an AWS CloudFront interface for creating a distribution, with fields for entering the origin domain, path, and access settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858474/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-cloudfront-distribution-interface.jpg)
</Frame>

### Configuring Additional Settings

Configure the following additional settings:

* Disable the Web Application Firewall (WAF) for this demonstration.
* Choose the appropriate price class—select "Use all edge locations" for a global cache.
* Custom SSL certificates are unnecessary for this demo.
* Set the **Default Root Object** to "index.html" to ensure users accessing the root URL are directed to the proper file.

<Frame>
  ![The image shows a configuration page for AWS CloudFront, focusing on Web Application Firewall (WAF) settings, with options to enable or disable security protections.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858475/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-cloudfront-waf-settings-config.jpg)
</Frame>

<Frame>
  ![The image shows a configuration page for creating a CloudFront distribution on the AWS Management Console, with options for SSL certificates, HTTP versions, logging, and IPv6 settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858477/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/cloudfront-distribution-configuration-aws.jpg)
</Frame>

Once the configuration is complete, click **Create Distribution**. During provisioning, CloudFront prompts you to update the S3 bucket policy to enable access to your files.

<Frame>
  ![The image shows an AWS CloudFront distribution management page, indicating a new distribution has been successfully created, with a notification to update the S3 bucket policy.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858478/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-cloudfront-distribution-management.jpg)
</Frame>

## Step 3: Updating the S3 Bucket Policy

To allow CloudFront to access your S3 files, update the bucket policy as follows:

1. In the CloudFront console, click **Copy Policy**.
2. Go to your S3 bucket’s **Permissions** tab.
3. Paste the copied policy into the Bucket Policy editor. An example policy appears as:

```json theme={null}
{
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::kodekloud-cloudfront-demo/*",
            "Condition": {}
        }
    ]
}
```

If you wish to restrict access to only the current CloudFront distribution, a more specific policy might be:

```json theme={null}
{
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::kodekloud-cloudfront-demo/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront:841860927337:distribution/E2D1BKS7RKY1GR"
                }
            }
        }
    ]
}
```

After pasting and saving the policy, CloudFront will securely link to your S3 bucket.

<Frame>
  ![The image shows an AWS CloudFront configuration screen where an origin domain is being set up with options for origin access control settings. There are fields for entering the origin domain name and path, and options for access control settings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858479/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-cloudfront-origin-configuration.jpg)
</Frame>

## Step 4: Testing the Distribution

Once CloudFront finishes deploying (this may take several minutes), confirm that your distribution’s state is "Enabled" from the CloudFront distributions list. Copy the distribution domain name provided by CloudFront.

By accessing the domain (with just a forward slash), CloudFront will serve the default root object—index.html. The first request retrieves files from S3, and subsequent requests are served from the CloudFront cache, greatly reducing load times.

<Frame>
  ![The image shows an AWS CloudFront distribution settings page, displaying details such as the distribution domain name, ARN, and settings like logging and HTTP versions.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858480/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-cloudfront-distribution-settings.jpg)
</Frame>

## Step 5: Understanding Cache Settings

By default, CloudFront caches content for 24 hours (86,400 seconds). To check these settings, edit the default behavior and click **View Policy** under Cache Key or Cache Policy Settings.

<Frame>
  ![The image shows an AWS CloudFront settings page, focusing on cache key and origin request configurations, with options for allowed HTTP methods and cache policies.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858481/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-cloudfront-cache-settings.jpg)
</Frame>

## Step 6: Demonstrating Cache Invalidation

To demonstrate cache invalidation, imagine updating a cached file. Suppose you have an image named "car.jpg" initially displaying a red car. If you upload an updated "car.jpg" (showing a blue car) to the S3 bucket, it will overwrite the current file.

<Frame>
  ![The image shows an AWS CloudFront settings page for a caching policy named "Managed-CachingOptimized," detailing TTL settings, cache key settings, and compression support options.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858482/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-cloudfront-managed-caching-policy.jpg)
</Frame>

Even after the update, CloudFront may continue showing the cached red image due to the set 24-hour TTL. To force CloudFront to pull the updated content, manually invalidate the cache:

1. In the CloudFront console, go to the **Invalidations** section and create a new invalidation.
2. Specify the object path to invalidate. You can use "/\*" to invalidate all files or target a specific file (e.g., "/images/car.jpg").

<Frame>
  ![The image shows an AWS CloudFront console displaying the "Behaviors" tab for a distribution, with details like path pattern, origin, and protocol policy. There is an option to create a new behavior.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858483/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-cloudfront-behaviors-console.jpg)
</Frame>

<Frame>
  ![The image shows an AWS CloudFront interface for creating an invalidation, where users can add object paths to remove from the cache. There are options to cancel or create the invalidation.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858484/notes-assets/images/AWS-Certified-Developer-Associate-CloudFront-Basics-Demo/aws-cloudfront-invalidation-interface.jpg)
</Frame>

Once the invalidation completes, refreshing your application should display the blue car image because CloudFront will fetch the latest version from S3.

## Conclusion

This demo has shown you how to configure an S3 bucket and set up an AWS CloudFront distribution to effectively serve and cache web application assets. We also covered how to update the S3 bucket policy to permit CloudFront access, understand cache TTL settings, and perform manual cache invalidation to ensure users receive the most updated content.

<Callout icon="lightbulb">
  For further reading on CloudFront and AWS architecture, check out the [AWS CloudFront Documentation](https://aws.amazon.com/cloudfront/).
</Callout>

Happy learning, and see you in the next article!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/d25d5e41-6379-4261-9036-c1d8017dbdab/lesson/54d6d761-e5bc-4460-a8d8-0276e29f0f0c" />
</CardGroup>
