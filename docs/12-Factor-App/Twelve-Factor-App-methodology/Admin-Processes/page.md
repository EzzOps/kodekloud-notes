# Admin Processes

Source: https://notes.kodekloud.com/docs/12-Factor-App/Twelve-Factor-App-methodology/Admin-Processes/page

This article discusses the importance of isolating administrative tasks from main application processes in the 12-Factor App methodology.

In this lesson, we delve into the final principle of the [12-Factor App](https://learn.kodekloud.com/user/courses/12-factor-app) methodology—admin processes. This principle emphasizes the importance of isolating one-off or periodic administrative tasks from the main application processes to ensure that these tasks run on an identical setup as the production environment.

Currently, our application leverages a Redis database to store the count of total visitors. However, there may be instances where the counter becomes inaccurate or requires a reset. In such cases, it is crucial to execute a one-time administrative task without disrupting the running application.

<Callout icon="lightbulb">
  Administrative tasks—such as resetting visitor counts, executing database migrations, or correcting specific user records—must be performed as isolated, one-off processes. This approach enables automation, scalability, and reproducibility while maintaining a production-like environment.
</Callout>

For example, to reset the visitor count stored in Redis, you can execute an admin script. In our setup, this might involve launching an additional Docker container that connects to the same Redis database and runs the reset script:

```python theme={null}
import os
from redis import Redis
