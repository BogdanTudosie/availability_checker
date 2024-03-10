Very simple solution using asyncio tasks to send periodic requests to a list of websites, find a specified text and log the activity.

Asyncio was the option of choice due to the ability of creating scheduled tasks every x seconds and not relying on tasks to complete hence the asynchronous approach.

Other approaches for this would have been creating a specific class to handle all of this.