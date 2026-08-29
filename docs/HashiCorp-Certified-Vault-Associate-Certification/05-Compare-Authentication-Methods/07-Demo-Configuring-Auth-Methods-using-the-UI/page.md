# Success! Enabled userpass auth method at: userpass/
```

Verify it’s enabled:

```bash theme={null}
vault auth list
# Path      Type      Accessor
# ----      ----      ---------
# token/    token     auth_token_...
# userpass/ userpass  auth_userpass_...
```

### 2. Enable `userpass` on a Custom Path

```bash theme={null}
vault auth enable -path=vault-course userpass
# Success! Enabled userpass auth method at: vault-course/
```

List both mounts:

```bash theme={null}
vault auth list
# Path           Type      Accessor
# ----           ----      ---------
# token/         token     auth_token_...
# userpass/      userpass  auth_userpass_...
# vault-course/  userpass  auth_userpass_...
```

## Disabling Auth Methods

> **triangle-alert** Disabling an auth method immediately revokes any credentials issued under that mount.

### 1. Remove the Default `userpass` Mount

```bash theme={null}
vault auth disable userpass
# Success! Disabled the auth method at: userpass/
```

Confirm removal:

```bash theme={null}
vault auth list
# Path           Type      Accessor
# ----           ----      ---------
# token/         token     auth_token_...
# vault-course/  userpass  auth_userpass_...
```

### 2. Clean Up the Custom Mount

```bash theme={null}
vault auth disable vault-course
# Success! Disabled the auth method at: vault-course/
```

Only the `token` backend remains:

```bash theme={null}
vault auth list
# Path      Type   Accessor
# ----      ----   ---------
# token/    token  auth_token_...
```

## Adding a Description When Mounting

Descriptions must be provided at mount time. Any existing mount must be disabled first.

```bash theme={null}
vault auth disable userpass
```

> **lightbulb** You cannot add or update a description on an existing mount. Always set it when you enable the backend.

```bash theme={null}
vault auth enable \
  -path=bryan \
  -description="Local credentials for Vault access" \
  userpass
# Success! Enabled userpass auth method at: bryan/
```

Verify the description:

```bash theme={null}
vault auth list
# Path   Type      Accessor             Description
# ----   ----      --------             -----------
# bryan/ userpass  auth_userpass_...     Local credentials for Vault access
# token/ token     auth_token_...        token based credentials
```

## Tuning an Auth Method

Adjust the default lease TTL for tokens issued via the `bryan` mount:

```bash theme={null}
vault auth tune \
  -default-lease-ttl=24h \
  bryan/
# Success! Tuned the auth method at: bryan/
```

## Configuring the `userpass` Backend

### Create a User in `bryan`

```bash theme={null}
vault write auth/bryan/users/krausen \
  password=vault \
  policies=bryan
# Success! Data written to: auth/bryan/users/krausen
```

### List and Read User Details

```bash theme={null}
vault list auth/bryan/users
# Keys
# ----
vault read auth/bryan/users/krausen
# Key                     Value
# ---                     -----
# policies                [bryan]
# token_bound_cidrs       []
# token_policies          [bryan]
# token_ttl               0s
# token_type              default
```

Different backends accept different parameters—for example, `approle` uses `role` instead of `users`.

## Example: Enabling and Configuring AppRole

1. **Enable the AppRole Method**

   ```bash theme={null}
   vault auth enable approle
   # Success! Enabled approle auth method at: approle/
   ```

2. **Create a Role with a 20-Minute Token TTL**

   ```bash theme={null}
   vault write auth/approle/role/bryan \
     token_ttl=20m \
     policies=bryan
   # Success! Data written to: auth/approle/role/bryan
   ```

> **lightbulb** AppRole is recommended for machine-to-machine authentication and automated workflows.

## Conclusion

You’ve learned how to:

* Enable and list Vault auth methods
* Disable mounts safely
* Add metadata (descriptions)
* Tune mount configurations
* Create and manage users in `userpass`
* Configure an AppRole backend

These CLI patterns apply to all Vault authentication backends—just adjust paths, parameters, and payloads to fit your use case.

## Links and References

* [Vault CLI Documentation](https://www.vaultproject.io/docs/commands/auth)
* [Userpass Auth Method](https://www.vaultproject.io/docs/auth/userpass)
* [AppRole Auth Method](https://www.vaultproject.io/docs/auth/approle)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/eebfb593-8885-43b0-a9ba-9f88af87092e/lesson/e69b59fd-06a5-464a-9bf3-5d3e85324e02)


# Demo Configuring Auth Methods using the UI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Compare-Authentication-Methods/Demo-Configuring-Auth-Methods-using-the-UI/page

Learn to configure authentication methods in HashiCorp Vault using its web UI through a step-by-step guide.

In this step-by-step guide, you’ll learn how to configure authentication methods in HashiCorp Vault via its web UI. We’ll cover:

| Step | Action                      | Description                                        |
| ---- | --------------------------- | -------------------------------------------------- |
| 1    | Logging in with Okta        | Authenticate using your Okta credentials           |
| 2    | Enabling a new auth method  | Mount the userpass plugin with customized settings |
| 3    | Creating a user             | Add credentials and assign policies                |
| 4    | Testing login via the CLI   | Verify access by obtaining a Vault token           |
| 5    | Disabling & editing methods | Manage or remove existing auth mounts              |

***

## 1. Logging in with Okta

1. Open the Vault UI and select **Okta** as the authentication method.
2. Enter your **Username** and **Password**, then click **Sign In**.
3. Optionally, choose to save your credentials for future sessions.

![The image shows a login page for "Vault" with fields for method, username, and password, and a "Sign In" button. The method selected is "Okta," and there are options for saving the password.](https://kodekloud.com/kk-media/image/upload/v1752878013/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Configuring-Auth-Methods-using-the-UI/vault-login-page-okta-sign-in.jpg)

After successful authentication, you’ll be redirected to the Vault dashboard.

***

## 2. Enabling a New Auth Method

Navigate to **Access → Auth Methods**, then click **Enable new method**. You’ll see categories for Generic, Cloud, and Infra authentication plugins:

![The image shows a web interface for enabling an authentication method in Vault, with options for Generic, Cloud, and Infra authentication types. Various methods like AppRole, AWS, Azure, and Kubernetes are available for selection.](https://kodekloud.com/kk-media/image/upload/v1752878014/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Configuring-Auth-Methods-using-the-UI/vault-authentication-methods-web-interface.jpg)

Select **Username & Password** (userpass) and click **Next**. Configure the mount options:

* **Path**: `vault`
* **Default TTL**: `30m`
* **Max TTL**: `24h`
* **Token Type**: `service` (default)
* **Description**: *My cool new Auth Method*

> **lightbulb** Default TTL controls how long issued tokens remain valid before renewal.

If you have Vault Enterprise, you can also enable **Seal Wrap** for enhanced security. When ready, click **Enable method**:

![The image shows a web interface for enabling a username and password authentication method in a Vault application, with various configuration options like path, description, and token type.](https://kodekloud.com/kk-media/image/upload/v1752878016/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Configuring-Auth-Methods-using-the-UI/vault-username-password-authentication-interface.jpg)

Your new userpass method is now mounted at `vault/`.

***

## 3. Creating a User via the UI

1. Go back to **Access → Auth Methods** and click on the **vault** mount (userpass).

2. Select **Create User**.

3. Fill out the form:
   * **Username**: `bob`
   * **Password**: `Bob is cool`
   * **Policies**: `bryan`, `default`

4. Click **Save**. The user `bob` is now created and associated with the specified policies.

![The image shows a user interface for creating a new user in a system, with fields for username, password, and token settings. It includes options for configuring generated token policies and settings.](https://kodekloud.com/kk-media/image/upload/v1752878016/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Configuring-Auth-Methods-using-the-UI/user-interface-create-new-user-settings.jpg)

***

## 4. Testing Login via the CLI

Set your Vault server address and an existing admin token (Okta):

```bash theme={null}
export VAULT_ADDR="https://your-vault-address:8200"
export VAULT_TOKEN="s.TEKrNn3Cv53pZdbPh8xg4TPu"
```

Then log in as `bob`:

```bash theme={null}
vault login -method=userpass username=bob password='Bob is cool'
```

If you encounter a permissions error, verify that policies and mount path are correct:

```plaintext theme={null}
Error logging in: error validating credentials: permission denied
```

On success, Vault returns a new client token.

***

## 5. Disabling and Editing Auth Methods

To manage existing mounts:

* **Disable**: Click the three-dot menu next to the method and choose **Disable**, then confirm deletion of all related data.
* **Edit**: Select **View/Edit** beside a method to update its configuration.

For example, updating Azure auth settings lets you change Tenant ID, Resource, and Environment:

![The image shows a configuration page for setting up Azure in a Vault application, with fields for Tenant ID, Resource, and Environment. There are options to save the configuration and view method options.](https://kodekloud.com/kk-media/image/upload/v1752878017/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Demo-Configuring-Auth-Methods-using-the-UI/azure-vault-configuration-page-settings.jpg)

> **triangle-alert** Disabling an auth method permanently removes its data. Make sure you’ve migrated or no longer need it before confirmation.

***

Configuring Vault auth methods via the UI simplifies access control management. You can rapidly enable plugins, define policies, onboard users, test logins, and remove methods without leaving your browser.

## Links and References

* [HashiCorp Vault Authentication](https://www.vaultproject.io/docs/auth)
* [Vault UI Overview](https://www.vaultproject.io/docs/upgrading/ui)
* [Okta Auth Method](https://www.vaultproject.io/docs/auth/okta)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/eebfb593-8885-43b0-a9ba-9f88af87092e/lesson/edecf4ab-342e-453d-9153-9d4d3ed0fc75)
