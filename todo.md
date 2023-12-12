# Todo List

## High priority
### Phase 3
- [x] Move profile stuff to it's own blueprint
- [x] Link profile nav item to profile page
- [x] Link wishlist page to profile page
- [x] Style authentication page
- [x] Remove or implement unimplemented content
  - [x] navbar
  - [x] homepage
  - [x] profile
  - [x] browse
  - [x] game page
  - [x] footer
- [x] Banner on profile page needs to be saved or there shouldn't be a banner at all.
### Phase 4
- [ ] Create sql database and populate it with data from games.csv
    - [x] Publisher
    - [x] Genre
    - [x] Tag
    - [x] Game
    - [ ] User
    - [ ] Review
    - [ ] Wishlist
  - [x] Browse and search features implemented with database
  - [ ] any updates to games details must be stored in database
  - [ ] User authentication should work with database
  - [ ] Users need to be saved/loaded to/from database
  - [ ] Reviews and ratings must be saved in database
  - [ ] Database stores wishlists, interactions with wishlist should be reflected in database.
  - [ ] All details in user profile page must be read from database.
  - [ ] Testing
    - [ ] database is correctly created and populated
      - [ ] all required tables exist
      - [ ] all tables are populated 
    - [ ] core functionality of orm code
      - [ ] validity of mapper
      - [ ] relationships
    - [ ] core functionality of repository implementation
      - [ ] add one/multiple games
      - [ ] retrieve one/multiple games 
      - [ ] search functionality


## Low priority
- [ ] Replace popularity with review score on browse page
- [ ] Swap out add to wishlist with remove from wishlist on game page when game is in users wishlist.
- [ ] Put the game info into chip form on browse page.
- [ ] Profile specific styling should be in its own file.