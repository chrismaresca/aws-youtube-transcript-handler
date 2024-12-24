# Serverless Python + AWS Lambda HTTP Post To Fetch YouTube Transcript

An AWS Lambda function to fetch a YouTube transcript.

## Configure Serverless

1. Install the `serverless-python-requirements` plugin if you don't have it already.

```bash
pnpm install serverless-python-requirements
```

2. Install the `serverless-plugin-resource-tagging` plugin if you don't have it already.

```bash
pnpm install serverless-plugin-resource-tagging
```

3. Install the `serverless-functions-base-path` plugin if you don't have it already.

```bash
pnpm install serverless-functions-base-path
```

4. Set the following environment variables (Everything except the OpenAI API key are already set in the `.env.sample` file. To use this file, rename it to `.env` with the following command

```bash
mv .env.sample .env
```

For a brief explanation of each environment variable, see below:

- **SERVICE_NAME**: The name of the service (default: youtube-transcript-service-v1)

- **LOG_LEVEL**: Logging level (default: DEBUG).

- **USE_PROXY**: Use a proxy to fetch the transcript (default: false).

- **PROXY_USERNAME**: The username for the proxy (default: none).

- **PROXY_PASSWORD**: The password for the proxy (default: none).

5. Update `serverless.yml` to include the `serverless-python-requirements` plugin.

6. Update `serverless.yml` to include the `serverless-plugin-resource-tagging` plugin.

7. Update `serverless.yml` to include the `serverless-functions-base-path` plugin.

8. Update the 'service' of the service in `serverless.yml` to your desired service name.

9. Logging is configured in `src/utils/logger.py` to output to stdout. This should work on AWS CloudWatch.

## Deploy Serverless

```bash
serverless deploy
```
