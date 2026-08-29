# Key Value Pair
Fruit: Apple
Vegetable: Carrot
Liquid: Water
Meat: Chicken
```

> **lightbulb** Remember to include a space after the colon to separate the key from its value.

To represent lists or arrays, first define the key and then use a dash to indicate each element. For example, to list some fruits and vegetables:

```yaml theme={null}
# Key Value Pair
Fruit: Apple
Vegetable: Carrot
Liquid: Water
Meat: Chicken

# Array / Lists
Fruits:
  - Orange
  - Apple
  - Banana

Vegetables:
  - Carrot
  - Cauliflower
  - Tomato
```

## Dictionaries (Maps)

A dictionary (or map) in YAML groups related properties under a single key. Consider this example, which shows the nutritional information for two fruits. Each fruit—Banana and Grapes—has its own properties such as calories, fat, and carbs:

```yaml theme={null}
# Dictionary / Map
Banana:
  Calories: 105
  Fat: 0.4 g
  Carbs: 27 g
Grapes:
  Calories: 62
  Fat: 0.3 g
  Carbs: 16 g
```

In YAML, the number of spaces before each property is essential. All properties within a dictionary must be aligned with consistent indentation. For example, the nutritional information for a banana is correctly represented with uniform indentation:

![The image shows a diagram of a banana's nutritional information, including calories (105), fat (0.4g), and carbs (27g), labeled as a "Dictionary/Map."](https://kodekloud.com/kk-media/image/upload/v1752884976/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Introduction-to-YAML/frame_180.jpg)

> **triangle-alert** Avoid adding extra spaces before properties (e.g., around "fat" and "carbs") as this could incorrectly nest them under the previous key (such as "Calories"), potentially causing a syntax error.

## Nested Structures

YAML makes it easy to define nested structures like lists containing dictionaries. For example, consider a list of fruits where each item includes its nutritional details:

```yaml theme={null}
# List containing dictionaries
Fruits:
  - Banana:
      Calories: 105
      Fat: 0.4 g
      Carbs: 27 g
  - Grape:
      Calories: 62
      Fat: 0.3 g
      Carbs: 16 g
```

A common question when learning YAML is determining when to use a dictionary versus a list. Data formats such as XML, JSON, and YAML are designed to represent a wide range of data—from organization employees and student records to details about cars in a manufacturing company.

For example, a single car object might be represented with a dictionary that outlines its properties such as color, model, transmission type, and price:

```yaml theme={null}
Color: Blue
Model:
  Name: Corvette
  Year: 1995
Transmission: Manual
Price: $20,000
```

If you need to represent multiple cars, each with detailed information, you would use a list of dictionaries, where each dictionary represents a car:

```yaml theme={null}
- Color: Blue
  Model:
    Name: Corvette
    Year: 1995
  Transmission: Manual
  Price: $20,000
- Color: Grey
  Model:
    Name: Corvette
    Year: 1995
  Transmission: Manual
  Price: $22,000
- Color: Red
  Model:
    Name: Corvette
    Year: 1995
  Transmission: Automatic
  Price: $20,000
- Color: Green
  Model:
    Name: Corvette
    Year: 1995
  Transmission: Manual
  Price: $23,000
- Color: Blue
  Model:
    Name: Corvette
    Year: 1995
  Transmission: Manual
  Price: $20,000
- Color: Black
  Model:
    Name: Corvette
    Year: 1995
  Transmission: Automatic
  Price: $25,000
```

This example clearly differentiates between using dictionaries, simple lists, and lists of dictionaries.

![The image compares data structures: dictionary, list, and list of dictionaries, using car attributes like color, model, transmission, and price.](https://kodekloud.com/kk-media/image/upload/v1752884977/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Introduction-to-YAML/frame_410.jpg)

## Key Points on Data Structures in YAML

Below are several key points to remember when working with YAML data structures:

| Data Structure   | Characteristics                                                                      | Example                    |
| ---------------- | ------------------------------------------------------------------------------------ | -------------------------- |
| Dictionary (Map) | An unordered collection; the order of properties does not affect the data's meaning. | Nutritional info of Banana |
| List (Array)     | An ordered collection; the sequence of items is significant.                         | List of Fruits             |
| Comments         | Any line starting with a hash (#) is considered a comment and ignored by the parser. | # This is a comment        |

Here’s an example of an unordered dictionary:

```yaml theme={null}
Banana:
  Calories: 105
  Fat: 0.4 g
  Carbs: 27 g
```

And this is an ordered list where the position of each item matters:

```yaml theme={null}
Fruits:
  - Orange
  - Apple
  - Banana
```

We are now ready to proceed to the coding exercises. Have fun exploring and working with YAML files!

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/9bcecdb4-c89c-439f-8590-cb55efa4f596/lesson/4af4cd4b-d22c-4cf8-b4b7-7a9d2a585e6a)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/9bcecdb4-c89c-439f-8590-cb55efa4f596/lesson/6204e403-2683-4bd4-b946-402cc61ff22a)


# Accessing storage endpoints

Source: https://notes.kodekloud.com/docs/Updated-AZ-104-Microsoft-Azure-Administrator/Administer-Azure-Storage/Accessing-storage-endpoints/page

Learn to construct and understand the endpoints required to access various services within an Azure storage account.

In this lesson, you'll learn how to construct and understand the endpoints required to access various services within an Azure storage account. Each storage service follows a consistent endpoint URL format, making it easy to integrate and manage your storage resources.

Every endpoint is built using the following structure:

```plaintext theme={null}
<protocol>://<storage account name>.<service>.core.windows.net
```

Here's what each element represents:

* **Protocol:** Either `HTTP` or `HTTPS`.
* **Storage Account Name:** The unique name you have chosen for your account.
* **Service:** Represents the Azure service you are accessing (e.g., blob, queue, file, or table).
* **Domain:** All endpoints end with `core.windows.net`, which is the default domain for Azure storage.

For example, if your storage account is named `KodeKloud`, the corresponding endpoints would be:

* **Blob Service:** kodekloud.blob.core.windows.net
* **Queue Service:** kodekloud.queue.core.windows.net
* **File Service:** kodekloud.file.core.windows.net
* **Table Service:** kodekloud.table.core.windows.net

> **lightbulb** If your preferred storage account name is already taken, consider modifying it by appending additional characters or using a custom domain. This approach can also reinforce your branding; for example, you might configure `blobs.codecloud.com` to point to `codecloud.blob.core.windows.net`.

![The image provides information on accessing storage endpoints for a storage account, showing the format for endpoint URLs and examples for different services like container, queue, file, and table. It also mentions using a custom domain with CNAME mapping.](https://kodekloud.com/kk-media/image/upload/v1752884371/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Accessing-storage-endpoints/storage-endpoints-url-format-examples.jpg)

In addition to direct URL access, several tools help manage your Azure storage resources effectively:

## Azure Storage Management Tools

| Tool                   | Description                                                                                                                                              | Example Command/Usage                                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Azure Storage Explorer | Desktop application that connects to your storage account, allowing you to drag and drop files, delete files, and manage data directly.                  | Launch the app and connect using your storage account credentials                                                      |
| Import Export Service  | Service for transferring large quantities of on-premises data (terabytes or more) into Azure. It enables secure data transfer via pre-configured drives. | Prepare drives, copy, encrypt, and ship them to an Azure Data Center for upload                                        |
| AZCopy                 | Command-line tool designed for fast and efficient data transfers within your storage account, and supports other cloud providers like GCP and AWS.       | `azcopy copy [source] [destination] [flags]` This command can be automated to handle disaster recovery data transfers. |

![The image shows a configuration guide for storage tools, featuring Azure Storage Explorer and an Import and Export Service interface.](https://kodekloud.com/kk-media/image/upload/v1752884372/notes-assets/images/Updated-AZ-104-Microsoft-Azure-Administrator-Accessing-storage-endpoints/azure-storage-tools-configuration-guide.jpg)

For example, the following command uses AZCopy to transfer data:

```bash theme={null}
azcopy copy [source] [destination] [flags]
```

This tool is especially useful for automating data workflows and migrating data between different cloud providers.

When managing your storage account via the Azure Portal, you can easily capture the endpoints for blob, file, queue, table services, and even static website hosting. Additionally, services like Data Lake Store—designed for analytics—offer their own respective endpoints.

Up next, we will explore how to configure Azure Blob Storage, building on the concepts discussed in this lesson.

> **lightbulb** For further reading on Azure storage, visit the [Azure Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/) and explore [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) for related containerized solutions.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-104-microsoft-azure-administrator/module/48d08f66-feb9-4bae-83b0-2e6aa34e24ae/lesson/1ccae4d6-20ed-4ebc-9042-ea47f2d66dbc)
