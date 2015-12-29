Forum notification : the user must be able to manage precisely which notifications he wants to receive. For example, he might choose to receive by mail all new posts in a given thread or in a given category. He can also manage notifications by localization : receive notifications only for threads that are followed by users living in the same area, or thread that speak about events in the area of the user.

## Schema
Each user has its "notification registry" storing all the information on what events trigger notifications :
- related to threads : the notification registry stores the list of threads followed by the user.
- categories : the list of categories followed by the user. If a user follows a category then he follow all threads in this category, and we update him about any modifcation/ new post in this category.
- area : the user selects if he wants to follow all "events" in the area.

## events
### thread
- New post
- Edited post

### category
- events in a thread
- new thread
- deleted thread
- edit category description

### area
- new localized thread.
- events in localized thread.
- new localized category.
- events in localized category.

## options
- real-time notifications
- per-period notification resumé
- notification vectors : in-app, e-mail, facebook message ? whatsapp message ?
See notifcations.encoding.NotificationsSettings