# S3 Versioning Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Storage/S3-Versioning-Demo/page

This lesson explores Amazon S3 versioning by creating a bucket, uploading files, and comparing behaviors with versioning enabled and disabled.

In this lesson, we explore how Amazon S3 versioning works by creating a bucket, uploading files, and observing the differences in behavior when versioning is disabled versus enabled.

## Creating a Bucket with Versioning Disabled

First, create a new S3 bucket named "versioning-demo" (or a similar name) using the default settings. Make sure that bucket versioning is disabled. With versioning off, file overwrites or deletions are permanent.

Next, open the bucket and upload a file. For this demo, we use a dummy text file named `file1.txt` containing:

```text theme={null}
this is version 1
```

This content easily identifies the file's version.

<Frame>
  ![The image shows an Amazon S3 console with a bucket named "kk-versioning-demo" and a Visual Studio Code window displaying a text file named "file1.txt" with the content "this is version 1".](https://kodekloud.com/kk-media/image/upload/v1752859806/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-console-visual-studio-code.jpg)
</Frame>

After verifying the file details in the S3 upload interface, proceed with the upload.

<Frame>
  ![The image shows an Amazon S3 upload interface where a file named "file1.txt" is ready to be uploaded to a bucket named "kk-versioning-demo." The file is 17.0 bytes in size.](https://kodekloud.com/kk-media/image/upload/v1752859807/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-upload-file1-kk-demo.jpg)
</Frame>

Once the file is uploaded, opening it within the bucket displays "this is version 1."

## Deleting the File with Versioning Disabled

When versioning is disabled, deleting a file removes it permanently. To demonstrate, select the file and click "Delete." Confirm the prompt for permanent deletion.

<Frame>
  ![The image shows an Amazon S3 interface for deleting objects, specifically a file named "file1.txt" with details like type, last modified date, and size. There is a prompt to confirm permanent deletion by typing "permanently delete."](https://kodekloud.com/kk-media/image/upload/v1752859808/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-delete-file-interface.jpg)
</Frame>

After deletion, the file is permanently removed. To continue the demonstration, re-upload `file1.txt` with the same content to restore it as version one.

<Frame>
  ![The image shows an Amazon S3 console displaying details of a file named "file1.txt," including its properties, S3 URI, and object URL. The bucket versioning is currently disabled.](https://kodekloud.com/kk-media/image/upload/v1752859810/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-file1txt-details.jpg)
</Frame>

## Overwriting a File (Versioning Disabled)

To show how file overwrites work without versioning, open your text file and change its content to indicate an updated version:

```text theme={null}
this is version 2
```

Save and re-upload the file to the S3 bucket. Since the file key remains the same, the new upload overwrites the existing file. When you view `file1.txt`, it now displays "this is version 2"; the original version one is permanently lost.

## Enabling Bucket Versioning

Now, let's enable bucket versioning to observe the changes in file management. Go to the bucket properties, navigate to the bucket versioning section, click "Edit," and enable versioning.

<Frame>
  ![The image shows the properties page of an Amazon S3 bucket named "kk-versioning-demo" in the AWS Management Console. It displays details about bucket versioning, tags, and default encryption settings, with options to edit these configurations.](https://kodekloud.com/kk-media/image/upload/v1752859811/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-bucket-properties.jpg)
</Frame>

With versioning enabled, re-upload the original file (`file1.txt`) with the content:

```text theme={null}
this is version 1
```

Although the file appears unchanged, the "Show versions" option now appears, revealing a unique version ID for the file. Each subsequent overwrite will create a new version.

To update the file, modify the content to indicate version two:

```text theme={null}
this is version 2
```

Upload the file again using the same key. If the console does not immediately reflect changes, click "Show versions" to see two entries: the older version (version one) and the latest version (version two).

<Frame>
  ![The image shows an Amazon S3 console with a bucket named "kk-versioning-demo" containing a single text file, "file1.txt," with details like version ID, last modified date, size, and storage class.](https://kodekloud.com/kk-media/image/upload/v1752859812/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-console-kk-versioning-demo.jpg)
</Frame>

You can verify each version by opening them: version two shows "this is version 2," while version one still contains "this is version 1." Next, modify the file for version three:

```text theme={null}
this is version 3
```

Upload the file again. Your bucket now contains three versions of the file, with version three as the current version returned when accessing `file1.txt`.

## Deleting with Versioning Enabled

With versioning active, file deletion behaves differently. Select `file1.txt` and click the "Delete" button. The confirmation prompt will now only ask for a simple delete confirmation rather than a permanent deletion.

<Frame>
  ![The image shows an Amazon S3 console interface for deleting objects, specifically a file named "file1.txt." It includes a confirmation prompt to type "delete" to proceed with the deletion.](https://kodekloud.com/kk-media/image/upload/v1752859813/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-delete-file-interface-2.jpg)
</Frame>

When you delete the file in this mode, Amazon S3 adds a delete marker instead of permanently removing the object. Although the file may appear deleted, all previous versions remain accessible by enabling "Show versions."

<Frame>
  ![The image shows an Amazon S3 bucket interface with a list of versioned objects named "file1.txt," displaying details like version ID, last modified date, size, and storage class.](https://kodekloud.com/kk-media/image/upload/v1752859814/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-bucket-versioned-objects.jpg)
</Frame>

<Callout icon="lightbulb">
  To restore the file, simply delete the delete marker. Select the marker and confirm its permanent deletion.
</Callout>

<Frame>
  ![The image shows an Amazon S3 interface for deleting objects, specifically a file named "file1.txt" with a prompt to confirm permanent deletion.](https://kodekloud.com/kk-media/image/upload/v1752859816/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-delete-file1txt.jpg)
</Frame>

You can also selectively delete a specific version (for example, version two) by choosing that version and confirming its permanent deletion. Once a version is deleted, it cannot be recovered.

## Suspending Bucket Versioning

It is important to note that once enabled, bucket versioning cannot be disabled—only suspended. To suspend versioning, return to the bucket properties, edit the versioning configuration, select "Suspend," and confirm.

<Frame>
  ![The image shows the "Edit Bucket Versioning" page in the Amazon S3 console, where users can enable or suspend versioning for a bucket. It includes options for multi-factor authentication and a warning about the impact of suspending versioning.](https://kodekloud.com/kk-media/image/upload/v1752859817/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/edit-bucket-versioning-amazon-s3.jpg)
</Frame>

Suspending versioning leaves all existing version entries intact. However, any new uploads for existing keys will be stored with a version ID of null. For example, update `file1.txt` to create version four:

```text theme={null}
this is version 4
```

After uploading, you'll notice the new version has a version ID of null. Subsequent updates (e.g., version five) will replace the file with a null version ID, though older versions remain stored in the bucket.

## Uploading a New Object with a Different Key

To see the behavior for objects with unique keys under suspended versioning, create and upload a new file named `file2.txt` with the content:

```text theme={null}
this is version 1
```

Since versioning is suspended, this file will be stored with a null version ID. If you later modify and upload `file2.txt` with new content:

```text theme={null}
this is version 2
```

The new upload will also have a null version ID and will replace the previous instance.

<Frame>
  ![The image shows an Amazon S3 bucket interface with a list of objects and a Visual Studio Code window displaying a text file with the content "this is version 5."](https://kodekloud.com/kk-media/image/upload/v1752859819/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-bucket-vscode-file.jpg)
</Frame>

## Multi-Factor Authentication (MFA) Delete

MFA Delete adds an extra layer of security by requiring multi-factor authentication for any changes to the versioning state. Note that MFA Delete can only be enabled via the AWS CLI or an SDK and is not available in the AWS Management Console. For more details, refer to the [AWS documentation](https://aws.amazon.com/documentation/).

## Clean Up

After completing this demonstration, clean up your S3 resources by ensuring all object versions have been shown and then deleting every object in the bucket before finally deleting the bucket.

<Frame>
  ![The image shows an Amazon S3 interface for deleting objects, listing several text files with details like version ID, type, last modified date, and size. There's a prompt to confirm permanent deletion by typing "permanently delete."](https://kodekloud.com/kk-media/image/upload/v1752859821/notes-assets/images/AWS-Certified-Developer-Associate-S3-Versioning-Demo/amazon-s3-delete-objects-interface.jpg)
</Frame>

This concludes the S3 versioning demonstration.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/e8ae2293-e16b-42d3-b32b-5c260a1f1e5d/lesson/e313dcef-1d9f-4d6b-99cb-d81e9b44b96c" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/e8ae2293-e16b-42d3-b32b-5c260a1f1e5d/lesson/c9d59b57-16b8-468d-912c-8d95d6a8d97c" />
</CardGroup>
