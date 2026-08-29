# Output: image: NGINX
```

An alternative and more common approach is to use pipelines by positioning the function name at the end of the variable. Pipelines allow you to chain multiple functions together, thereby enhancing readability and flexibility in your templates.

Consider the following example, which converts the repository value to uppercase and then encloses it in quotes:

```helm theme={null}
{{ .Values.image.repository | upper | quote }}
# Output: image: "NGINX"
```

You can further extend this technique by chaining additional functions. For example, if you need to shuffle the characters after converting to uppercase and enclosing them in quotes, you can achieve that with the following pipeline:

```helm theme={null}
{{ .Values.image.repository | upper | quote | shuffle }}
```

> **lightbulb** Remember that pipelines not only make your templating code cleaner but also allow you to perform complex transformations in a readable and efficient manner.

Practice using functions and pipelines in your own projects to fully grasp their potential. Happy coding, and see you in the next lesson!

- [Watch Video](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/b90a4aa4-31b5-43d3-a7aa-383d48c50db0/lesson/752e5734-8f48-44fa-a936-e9aff83e9cbd)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/b90a4aa4-31b5-43d3-a7aa-383d48c50db0/lesson/4dc824a1-4d39-4f27-b52d-1026e2647718)


# Ranges

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Helm-Charts-Anatomy/Ranges/page

This article explores using loops and ranges in templating to dynamically generate configuration files.

In this article, we explore how to use loops and ranges to dynamically generate configuration files using templating. Loops, such as the "for" loop in many programming languages, execute a block of code repetitively by iterating over a collection of data. For example, consider the following simple loop which prints numbers from 1 to 10:

```plaintext theme={null}
for i in 1 to 10:
    print i
end
```

Each iteration updates the value of i sequentially, and the print statement is executed 10 times to display numbers 1 through 10.

## ConfigMap Template Example

Assume you have a list of regions defined in a YAML values file as follows:

```yaml theme={null}
regions:
  - ohio
  - newyork
  - ontario
  - london
  - singapore
  - mumbai
```

The objective is to create a ConfigMap template that automatically populates the regions section with these values. A basic ConfigMap template might initially look like this:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: RELEASE-NAME-regioninfo
data:
  regions:
    - "ohio"
    - "newyork"
    - "ontario"
    - "london"
    - "singapore"
    - "mumbai"
```

To generalize this template, start with a structure where the regions list is left empty. Notice the metadata includes a dynamic release name using templating syntax:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-regioninfo
data:
  regions:
```

## Using the Range Operator

Next, iterate over the list of regions from the values file by employing the `range` operator. The process involves looping through each region, where the current scope (represented by a dot) contains the region value. Initially, you might set up the loop as follows, which inserts a dash for each item:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-regioninfo
data:
  regions:
    {{- range .Values.regions }}
    -
    {{- end }}
```

> **lightbulb** At this stage, the actual region values are not included yet. The loop only creates a list item placeholder.

To include the actual region value, simply refer to the current value within the loop:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-regioninfo
data:
  regions:
    {{- range .Values.regions }}
    - {{ . }}
    {{- end }}
```

When rendered with the sample values, the output will be:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: RELEASE-NAME-regioninfo
data:
  regions:
    - ohio
    - newyork
    - ontario
    - london
    - singapore
    - mumbai
```

## Quoting Each Region Name

If your requirement specifies that each region name must be enclosed in quotes, you can pipe the value through a quoting function. The updated loop looks like this:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-regioninfo
data:
  regions:
    {{- range .Values.regions }}
    - {{ . | quote }}
    {{- end }}
```

This final version ensures that every region is encapsulated in quotes.

> **lightbulb** By mastering loops and ranges in templating, you can dynamically and efficiently generate Kubernetes ConfigMaps and other configuration files. Advanced templating techniques build on these basics to provide more flexible and powerful configuration options.

- [Watch Video](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/b90a4aa4-31b5-43d3-a7aa-383d48c50db0/lesson/b443e8eb-2b6e-4c80-9b0f-44a97478bb81)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/helm-for-beginners/module/b90a4aa4-31b5-43d3-a7aa-383d48c50db0/lesson/dacf089e-a7a6-46aa-88a4-0f73d2f0c4de)
