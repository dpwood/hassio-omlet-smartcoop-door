# hassio-omlet-smartcoop-door

Home Assistant integration to monitor and control an Omlet Smart Coop Door

The [Smart Automatic Chicken Coop Door](https://www.omlet.co.uk/smart-automatic-chicken-coop-door-opener/) by Omlet, allows your chicken coop door and lighting to be automated and managed via a handy app.

This integration adds some of those most valuable 'smart' features to Home Assistant:

- See the door's position and change it.
- Light switch
- Battery level

The Omlet server is **polled**, using their official API, to get the latest status of your devices.

Also supports **cloud push** using Omlet's webhooks. Home Assistant can be notified in real-time of any changes without needing to wait for a poll.

## Configuration

### API Key

Accessing the Omlet API requires an API Key. These are free and limitless:

1. Login to your Omlet Account at https://smart.omlet.com/developers/login
2. Under [API Keys](https://smart.omlet.com/developers/my/api-keys), generate a new key. Copy the newly generated token, that's your API Key that'll you'll need to enter when adding this integration.

### Webhooks

If your HA instance is accessible via the internet, then you can be notified of events in real-time rather than relying on polling.

Create a webhook

1. Visit [Manage Webhooks](https://smart.omlet.com/developers/my/webhooks) in the Omlet Developer Portal.
2. The URL will be [your hostname]**/api/webhook/omlet_smart_coop**
3. Add whatever events you want to track. Ctrl+Click to select multiple events.
4. Specify an arbitrary token. This token will be included in the webhooks to verify the authenticity of the sender.
5. The Provide this token when prompted for a webhook_token during the integration configuration.

During setup of this integration, you will be prompted for a webhook_token. Provide the same token you used when creating the webhook. If the tokens do not match, the notifcations will be ignored.
