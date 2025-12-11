# Todos

- [x] Session Management
  - [x] Register and Login API's
  - [x] DB setup for session management sqlite + SQLAlchemy
  - [x] UI pages for register and login
- [ ] Story tag selection
  - [x] API to get available story tags
  - [x] API to post selected story tag (fantasy, romance etc..) and generate base for the story.
  - [x] Link generated story base to a user
  - [ ] Integrate vector db for RAG. Store generated story in it
        Need to rework this: store world settings, locations and characters separately
  - [ ] UI for tag selection
- [ ] User stories selection
  - [ ] UI element (sidebar) to display all stories of a user
  - [ ] API to get all stories of a user
  - [ ] UI element to select and display story elements (characters, kingdoms, etc..)
- [ ] User input loop
  - [ ] UI for user chat
  - [x] API to process user input, generate response and store story log
        Future scope: shift to using SSE
  - [ ] UI element to display the entire story log
- [ ] Frontend and backend docker setup
- [ ] Integrate logging
