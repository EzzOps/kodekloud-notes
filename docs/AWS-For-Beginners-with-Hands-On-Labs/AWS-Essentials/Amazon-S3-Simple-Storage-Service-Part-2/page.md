# Amazon S3 Simple Storage Service Part 2

Source: https://notes.kodekloud.com/docs/AWS-For-Beginners-with-Hands-On-Labs/AWS-Essentials/Amazon-S3-Simple-Storage-Service-Part-2/page

Guide to inspecting and managing Amazon S3 objects in the console covering metadata, permissions, uploads, copies, deletions, prefixes, and bucket behaviors

Let’s inspect an object in Amazon S3 and walk through the key information available for each object, how console operations work, and the important behaviors to remember when uploading, copying, or deleting objects.

When you open an object in the S3 console you’ll immediately see basic properties: the bucket region, object size, and last modified timestamp. The console also displays the object key (its name inside the bucket), the object's ARN, the ETag, and the object URL that can be used to retrieve it. Additional per-object settings include storage class, server-side encryption, object lock state, checksums, and tags — these attributes can vary between objects even within the same bucket.

<Frame>
  <img alt="A screenshot of an Amazon S3 object management overview showing bucket properties and management configurations; a warning indicates bucket versioning is disabled with an &#x22;Enable Bucket Versioning&#x22; button. Object metadata (size, type, and object URL) is visible near the top." />
</Frame>

Many of those per-object settings are shown in more detail on the object details page. From there you can view and edit metadata and tags, check the object lock status, and inspect or modify additional checksum fields and encryption information.

<Frame>
  <img alt="A screenshot of an AWS S3 console object details page showing sections for Additional checksums, Tags, Metadata (Content-Type: image/jpeg), and Object Lock status (Disabled). The page includes Edit buttons and a note that Object Lock cannot be enabled after bucket creation." />
</Frame>

Access behavior and authenticated requests

If you click the Object URL in a browser, whether the object is accessible depends on its permissions. For a private object, an unauthenticated (anonymous) request returns an Access Denied response like this:

```xml theme={null}
<?xml version="1.0" encoding="UTF-8"?>
<Error>
  <Code>AccessDenied</Code>
  <Message>Access Denied</Message>
  <RequestId>PVYKMASZ2ZWJBJDYG</RequestId>
  <HostId>[SECRET_REDACTED]=</HostId>
</Error>
```

This illustrates that S3 objects are private by default. To view a private object from the console use the Open or Download actions — these use temporary, authenticated URLs tied to your console session. To make content publicly reachable you must explicitly allow access (for example via a bucket policy, object ACL, or by enabling static website hosting with appropriate permissions).

Folders in the console are key prefixes (not real directories)

Although the console shows a folder-like UI, S3 is a flat object store. “Folders” are simply prefixes in the object key. Creating a folder named food effectively creates the prefix food/ that will be part of any object key you upload into that pseudo-folder.

<Frame>
  <img alt="A screenshot of the Amazon S3 web console for the bucket &#x22;kk-demo-123&#x22;, showing one object listed (pexels-julio-nery-1687147.jpg) and UI controls like Create folder and Upload." />
</Frame>

Uploading multiple files shows progress and status

When uploading several files into a prefix the console shows per-file progress and an overall transfer indicator. Large, high-resolution images will take longer to upload based on your network conditions and the file sizes.

<Frame>
  <img alt="A screenshot of the Amazon S3 web console showing an upload status page with a progress bar (21%) and a summary for destination s3://kk-demo-123/food/. The files list shows image uploads (burger.jpg, pizza.jpg, sandwich.jpg, steak.jpg) with sizes and upload statuses." />
</Frame>

Common S3 object identifiers

Below are the typical identifiers S3 presents for an object (URI, ARN, ETag, HTTP URL, and the key). This table uses the example values from the screenshots to clarify each identifier’s purpose.

| Identifier type | Purpose                                            | Example                                                                                                      |
| --------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| S3 URI          | Console/CLI friendly object URI                    | s3://kk-demo-123/food/burger.jpg                                                                             |
| ARN             | Global resource name used in IAM policies          | arn:aws:s3:::kk-demo-123/food/burger.jpg                                                                     |
| ETag            | Content hash (often MD5 for non-multipart objects) | 755f2e777b54bcc687028946a253404d                                                                             |
| HTTPS URL       | Direct object URL for GET requests                 | [https://kk-demo-123.s3.amazonaws.com/food/burger.jpg](https://kk-demo-123.s3.amazonaws.com/food/burger.jpg) |
| Object key      | The key string stored in S3 (includes prefix)      | food/burger.jpg                                                                                              |

Because the console renders objects with the same prefix together, it appears as if they live in folders — but they are just objects with key names containing slashes.

If you attempt to open the object URL as an unauthenticated user, you will get the Access Denied XML shown earlier. Using the console Open button retrieves the object via your authenticated session credentials.

Deleting objects

Deleting an object is as straightforward as uploading: select the object and choose Delete. The console prompts you to confirm the deletion (typically by typing “permanently delete”) to prevent accidental removals. In buckets without versioning enabled, deletion permanently removes the object.

<Frame>
  <img alt="A screenshot of the Amazon S3 &#x22;Delete objects&#x22; confirmation page showing a listed file (pexels-julio-nery-1687147.jpg) in the kk-demo-123 bucket. A text input prompts the user to type &#x22;permanently delete&#x22; to confirm deletion." />
</Frame>

After a successful deletion the console shows a success banner and a summary of the operation.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the &#x22;Delete objects: status&#x22; page with a green banner indicating one object (2.7 MB) was successfully deleted and zero failures. The summary and an empty &#x22;Failed to delete&#x22; list are visible." />
</Frame>

Moving or copying objects (change the key)

Moving an object in S3 is implemented under the hood as a copy to the new key followed by a delete of the source object. To move or copy an object you provide the full destination path (the destination key). The console helps by pre-populating the destination prefix and showing options such as encryption behavior for the copied object.

<Frame>
  <img alt="A screenshot of the Amazon S3 console showing the &#x22;Destination&#x22; settings for copying objects, with a destination bucket path s3://kk-demo-123/food/test/ and the destination prefix &#x22;food/test/&#x22;. The top of the page shows informational bullet points about copying objects and encryption." />
</Frame>

Deleting a bucket: must be empty first

A bucket must be empty before it can be deleted. If you try to delete a non-empty bucket, the console will prevent deletion and show a warning. The UI provides an option to empty the bucket (permanently deleting all objects) before you confirm the bucket deletion by typing its name.

<Frame>
  <img alt="A screenshot of the Amazon S3 console on the &#x22;Delete bucket&#x22; page showing a red error banner that the bucket is not empty. The page asks the user to type the bucket name &#x22;kk-demo-123&#x22; to confirm deletion and the Delete bucket button is disabled." />
</Frame>

When you trigger an empty operation via the console you’ll typically need to confirm one more time (by typing “permanently delete” or the bucket name depending on the prompt). After the bucket is emptied, you can permanently delete the empty bucket by entering its name into the confirmation field.

<Callout icon="lightbulb">
  S3 recap: objects are stored in a flat namespace and identified by keys (which can include slashes to emulate folders). By default, buckets and objects are private — change permissions (bucket policies, ACLs, or object-level settings) to grant public access. If bucket versioning is disabled, deleting an object permanently removes it.
</Callout>

Links and references

* [Amazon S3 documentation — Overview](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [Amazon S3 object key name considerations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html)
* [Controlling access to Amazon S3 resources (IAM policies, bucket policies, ACLs)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-controls.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/d28d64dd-cbb1-45ed-83c4-e8d4b0b0d08b/lesson/7a985991-7238-406a-aad7-75e86682e644" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/d28d64dd-cbb1-45ed-83c4-e8d4b0b0d08b/lesson/da40c2da-86d7-4b8b-8d24-747177b20379" />
</CardGroup>
