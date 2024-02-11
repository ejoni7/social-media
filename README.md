Hi 👋
This is my first django project. It has 3 apps:

# accounts

   It countains all methods that I wrote for login and register .
   Also I defined AbstractUser for it.For both super_user and user
   "is_active" field is 'False' by default. So you need to active 
   the user after you create superuser by 'python manage.py shell'
   .Also for public users, You need to active a sms api servise 
   for it according to your regen. but for test, You can active 
   it by the superuser login in admin panel.
   Authentications are by phone and email
   
# direct
   THis app handles all conection methods. It handles all speaches
   between users they can see the notif if they have a new one .
   They can block the user and also they can reply to them
   
# topic

   This app has a perform like a Explore in instagram. One person
   creates a topic about what he likes to talk about. There is a 
   home page that users can select which topic they like to take 
   a part on it. When they select a topic they can see the main 
   topic and other users replies to . they can like and dislike 
   I handle it by 'HttpResponse' but it needs to handle with 
   javascript.

>> I wrote this with a old template so You should change it if
   you want to use as a profesional site. Also all messages and
   placeholders are persion. So you need to convert them to
   English, if you want to use

📡 If you had any question you can ask form me at :
   linkedin.com/in/ejmin-yaghoubian-01450324a
