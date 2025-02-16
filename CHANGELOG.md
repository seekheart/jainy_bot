# Jainy Bot Changelog

## Version v1.2.2

**Fixes**

- Another fix attempt at docker image not publishing by entering full docker qualifier tag

## Version v1.2.1

**Devops**

- Fix attempt at publishing docker hub image

## Version v1.2.0

**Features**
- Refactored the role reaction to be configurable
- Added role command to add/reload roles for assignment via assign
- Added ability for bot to auto display assignable roles

## Version v1.1.1

**Fixes**

- Fixed synchronous code blocking discord health check

**Dev Deps**

- removed requests lib for aiohttp to handle async requests

## Version v1.1.0
**Features**
- Added dalle command to generate images via ai

**Dev Deps**
- added requests for api calls

## Version v1.0.0
**Features**
- Moderation commands like kick, ban, unban, etc with audit log posted in a channel (configurable)
- Borb command for fun
- Clean command to purge messages by a user
- Uptime command to determine how long bot has been running
- Role assignment by emoji reaction
- Help command to see what commands are available and what they do
- Configuration via environment variables or `.env` file
