# Project 4 <!-- omit in toc -->

# Table of Contents <!-- omit in toc -->

<b>
Overview

- [1. Features](#1-features)
- [2. User Stories reviewed against UX Planes and Manual Testing](#2-user-stories-reviewed-against-ux-planes-and-manual-testing)
  - [2.1. Site Administration](#21-site-administration)
  - [2.2. User Profile](#22-user-profile)
    - [2.2.1. As a returning user,  I need to be able to sign up and login before I can manipulate my content with CRUD](#221-as-a-returning-user--i-need-to-be-able-to-sign-up-and-login-before-i-can-manipulate-my-content-with-crud)
  - [2.3. User Navigation](#23-user-navigation)
  - [2.4. User Content Management](#24-user-content-management)
    - [2.4.1. As a returning user,  I need to create posts in order to share content.](#241-as-a-returning-user--i-need-to-create-posts-in-order-to-share-content)
    - [2.4.2. As a returning user,  I need to read blog posts in a simple gallery view in order to share content](#242-as-a-returning-user--i-need-to-read-blog-posts-in-a-simple-gallery-view-in-order-to-share-content)
    - [2.4.3. As a returning user,  I need to delete posts so I can feel in control of what I share](#243-as-a-returning-user--i-need-to-delete-posts-so-i-can-feel-in-control-of-what-i-share)
    - [2.4.4. As a returning user,  I need to update posts so I can feel in control of what I share and address typos.](#244-as-a-returning-user--i-need-to-update-posts-so-i-can-feel-in-control-of-what-i-share-and-address-typos)
  - [2.5. Content Interaction](#25-content-interaction)
    - [2.5.1. As a user,  I'd like to be able to like posts so I can show my appreciation for the content.](#251-as-a-user--id-like-to-be-able-to-like-posts-so-i-can-show-my-appreciation-for-the-content)
    - [2.5.2. As a user,  I'd like to be able to comment on posts so I can engage with the content creator and other users.](#252-as-a-user--id-like-to-be-able-to-comment-on-posts-so-i-can-engage-with-the-content-creator-and-other-users)
    - [2.5.3. As a user,  I'd like to be able to share posts so I can share the content with my friends.](#253-as-a-user--id-like-to-be-able-to-share-posts-so-i-can-share-the-content-with-my-friends)
    - [2.5.4. As a user,  I'd like to be able to search for posts so I can find content that interests me.](#254-as-a-user--id-like-to-be-able-to-search-for-posts-so-i-can-find-content-that-interests-me)
    - [2.5.5. As a user,  I'd like to be able to bookmark posts so I can find content that interests me.](#255-as-a-user--id-like-to-be-able-to-bookmark-posts-so-i-can-find-content-that-interests-me)
  - [2.6. Accessibility](#26-accessibility)
    - [2.6.1. As a returning user,  I’d like to be able to use the site with a keyboard so I can navigate the site without a mouse.](#261-as-a-returning-user--id-like-to-be-able-to-use-the-site-with-a-keyboard-so-i-can-navigate-the-site-without-a-mouse)
  - [2.7. Security](#27-security)
    - [2.7.1. As a returning user,  I’d like to log in with Google so my experience can be smoother and it is easier to remember my credentials.](#271-as-a-returning-user--id-like-to-log-in-with-google-so-my-experience-can-be-smoother-and-it-is-easier-to-remember-my-credentials)
    - [2.7.2. As a returning user,  I'd like to be able to reset my password so I can regain access to my account if I forget my password.](#272-as-a-returning-user--id-like-to-be-able-to-reset-my-password-so-i-can-regain-access-to-my-account-if-i-forget-my-password)
    - [2.7.3. As a returning user,  I'd like to be able to log out so I can protect my account from unauthorised access.](#273-as-a-returning-user--id-like-to-be-able-to-log-out-so-i-can-protect-my-account-from-unauthorised-access)
    - [2.7.4. As a returning user,  I'd like to be able to delete my account so I can protect my account from unauthorised access.](#274-as-a-returning-user--id-like-to-be-able-to-delete-my-account-so-i-can-protect-my-account-from-unauthorised-access)
    - [2.7.5. As a returning user,  I'd like to be able to report inappropriate content.](#275-as-a-returning-user--id-like-to-be-able-to-report-inappropriate-content)
  - [2.8. Responsive Design](#28-responsive-design)
    - [2.8.1. As a returning user,  I’d like to browse a gallery / thumbnail view so I can engage on different levels.](#281-as-a-returning-user--id-like-to-browse-a-gallery--thumbnail-view-so-i-can-engage-on-different-levels)
    - [2.8.2. As a returning user,  I'd like the site to be responsive so I can use it on different devices.](#282-as-a-returning-user--id-like-the-site-to-be-responsive-so-i-can-use-it-on-different-devices)
  - [2.9. User Experience](#29-user-experience)
    - [2.9.1. As a returning user,  I want a theme that is specific, consistent and will appeal to my personal interests](#291-as-a-returning-user--i-want-a-theme-that-is-specific-consistent-and-will-appeal-to-my-personal-interests)
    - [2.9.2. As a returning user,  I want a visual design that is consistent and appeals to my target age group](#292-as-a-returning-user--i-want-a-visual-design-that-is-consistent-and-appeals-to-my-target-age-group)
    - [2.9.3. As a returning user,  I'd like to see UX evokes a positive emotional response with colour, animation and sound.](#293-as-a-returning-user--id-like-to-see-ux-evokes-a-positive-emotional-response-with-colour-animation-and-sound)
    - [2.9.4. As a returning user,  I need to be able to navigate the site comfortably so I can find content that interests me.](#294-as-a-returning-user--i-need-to-be-able-to-navigate-the-site-comfortably-so-i-can-find-content-that-interests-me)
- [3. Automatic Testing](#3-automatic-testing)
- [4. Issues and Bugs](#4-issues-and-bugs)
- [5. Acknowledgement and credits](#5-acknowledgement-and-credits)

</b>

Table of contents

- [1. Features](#1-features)
- [2. User Stories reviewed against UX Planes and Manual Testing](#2-user-stories-reviewed-against-ux-planes-and-manual-testing)
  - [2.1. Site Administration](#21-site-administration)
  - [2.2. User Profile](#22-user-profile)
    - [2.2.1. As a returning user,  I need to be able to sign up and login before I can manipulate my content with CRUD](#221-as-a-returning-user--i-need-to-be-able-to-sign-up-and-login-before-i-can-manipulate-my-content-with-crud)
  - [2.3. User Navigation](#23-user-navigation)
  - [2.4. User Content Management](#24-user-content-management)
    - [2.4.1. As a returning user,  I need to create posts in order to share content.](#241-as-a-returning-user--i-need-to-create-posts-in-order-to-share-content)
    - [2.4.2. As a returning user,  I need to read blog posts in a simple gallery view in order to share content](#242-as-a-returning-user--i-need-to-read-blog-posts-in-a-simple-gallery-view-in-order-to-share-content)
    - [2.4.3. As a returning user,  I need to delete posts so I can feel in control of what I share](#243-as-a-returning-user--i-need-to-delete-posts-so-i-can-feel-in-control-of-what-i-share)
    - [2.4.4. As a returning user,  I need to update posts so I can feel in control of what I share and address typos.](#244-as-a-returning-user--i-need-to-update-posts-so-i-can-feel-in-control-of-what-i-share-and-address-typos)
  - [2.5. Content Interaction](#25-content-interaction)
    - [2.5.1. As a user,  I'd like to be able to like posts so I can show my appreciation for the content.](#251-as-a-user--id-like-to-be-able-to-like-posts-so-i-can-show-my-appreciation-for-the-content)
    - [2.5.2. As a user,  I'd like to be able to comment on posts so I can engage with the content creator and other users.](#252-as-a-user--id-like-to-be-able-to-comment-on-posts-so-i-can-engage-with-the-content-creator-and-other-users)
    - [2.5.3. As a user,  I'd like to be able to share posts so I can share the content with my friends.](#253-as-a-user--id-like-to-be-able-to-share-posts-so-i-can-share-the-content-with-my-friends)
    - [2.5.4. As a user,  I'd like to be able to search for posts so I can find content that interests me.](#254-as-a-user--id-like-to-be-able-to-search-for-posts-so-i-can-find-content-that-interests-me)
    - [2.5.5. As a user,  I'd like to be able to bookmark posts so I can find content that interests me.](#255-as-a-user--id-like-to-be-able-to-bookmark-posts-so-i-can-find-content-that-interests-me)
  - [2.6. Accessibility](#26-accessibility)
    - [2.6.1. As a returning user,  I’d like to be able to use the site with a keyboard so I can navigate the site without a mouse.](#261-as-a-returning-user--id-like-to-be-able-to-use-the-site-with-a-keyboard-so-i-can-navigate-the-site-without-a-mouse)
  - [2.7. Security](#27-security)
    - [2.7.1. As a returning user,  I’d like to log in with Google so my experience can be smoother and it is easier to remember my credentials.](#271-as-a-returning-user--id-like-to-log-in-with-google-so-my-experience-can-be-smoother-and-it-is-easier-to-remember-my-credentials)
    - [2.7.2. As a returning user,  I'd like to be able to reset my password so I can regain access to my account if I forget my password.](#272-as-a-returning-user--id-like-to-be-able-to-reset-my-password-so-i-can-regain-access-to-my-account-if-i-forget-my-password)
    - [2.7.3. As a returning user,  I'd like to be able to log out so I can protect my account from unauthorised access.](#273-as-a-returning-user--id-like-to-be-able-to-log-out-so-i-can-protect-my-account-from-unauthorised-access)
    - [2.7.4. As a returning user,  I'd like to be able to delete my account so I can protect my account from unauthorised access.](#274-as-a-returning-user--id-like-to-be-able-to-delete-my-account-so-i-can-protect-my-account-from-unauthorised-access)
    - [2.7.5. As a returning user,  I'd like to be able to report inappropriate content.](#275-as-a-returning-user--id-like-to-be-able-to-report-inappropriate-content)
  - [2.8. Responsive Design](#28-responsive-design)
    - [2.8.1. As a returning user,  I’d like to browse a gallery / thumbnail view so I can engage on different levels.](#281-as-a-returning-user--id-like-to-browse-a-gallery--thumbnail-view-so-i-can-engage-on-different-levels)
    - [2.8.2. As a returning user,  I'd like the site to be responsive so I can use it on different devices.](#282-as-a-returning-user--id-like-the-site-to-be-responsive-so-i-can-use-it-on-different-devices)
  - [2.9. User Experience](#29-user-experience)
    - [2.9.1. As a returning user,  I want a theme that is specific, consistent and will appeal to my personal interests](#291-as-a-returning-user--i-want-a-theme-that-is-specific-consistent-and-will-appeal-to-my-personal-interests)
    - [2.9.2. As a returning user,  I want a visual design that is consistent and appeals to my target age group](#292-as-a-returning-user--i-want-a-visual-design-that-is-consistent-and-appeals-to-my-target-age-group)
    - [2.9.3. As a returning user,  I'd like to see UX evokes a positive emotional response with colour, animation and sound.](#293-as-a-returning-user--id-like-to-see-ux-evokes-a-positive-emotional-response-with-colour-animation-and-sound)
    - [2.9.4. As a returning user,  I need to be able to navigate the site comfortably so I can find content that interests me.](#294-as-a-returning-user--i-need-to-be-able-to-navigate-the-site-comfortably-so-i-can-find-content-that-interests-me)
- [3. Automatic Testing](#3-automatic-testing)
- [4. Issues and Bugs](#4-issues-and-bugs)
- [5. Acknowledgement and credits](#5-acknowledgement-and-credits)


# 1. Features

# 2. User Stories reviewed against UX Planes and Manual Testing

The user stories are organised by EPICS. They can be summarised here:

- Site Administration
- User Profile
- User Navigation
- Content Management
- Content Interaction
- Responsive Design
- User Experience
- Accessibility

## 2.1. Site Administration

## 2.2. User Profile

### 2.2.1. As a returning user, <!-- omit in toc--> I need to be able to sign up and login before I can manipulate my content with CRUD

## 2.3. User Navigation


## 2.4. User Content Management

### 2.4.1. As a returning user, <!-- omit in toc--> I need to create posts in order to share content.
### 2.4.2. As a returning user, <!-- omit in toc--> I need to read blog posts in a simple gallery view in order to share content
### 2.4.3. As a returning user, <!-- omit in toc--> I need to delete posts so I can feel in control of what I share
### 2.4.4. As a returning user, <!-- omit in toc--> I need to update posts so I can feel in control of what I share and address typos.

## 2.5. Content Interaction

### 2.5.1. As a user, <!-- omit in toc --> I'd like to be able to like posts so I can show my appreciation for the content.
### 2.5.2. As a user, <!-- omit in toc --> I'd like to be able to comment on posts so I can engage with the content creator and other users.
### 2.5.3. As a user, <!-- omit in toc --> I'd like to be able to share posts so I can share the content with my friends.
### 2.5.4. As a user, <!-- omit in toc --> I'd like to be able to search for posts so I can find content that interests me.
### 2.5.5. As a user, <!-- omit in toc --> I'd like to be able to bookmark posts so I can find content that interests me.

## 2.6. Accessibility
### 2.6.1. As a returning user, <!-- omit in toc--> I’d like to be able to use the site with a keyboard so I can navigate the site without a mouse.
- As a returning user I'd like to be able to use the site in dark and light mode.

## 2.7. Security
### 2.7.1. As a returning user, <!-- omit in toc--> I’d like to log in with Google so my experience can be smoother and it is easier to remember my credentials.
### 2.7.2. As a returning user, <!-- omit in toc--> I'd like to be able to reset my password so I can regain access to my account if I forget my password.
### 2.7.3. As a returning user, <!-- omit in toc--> I'd like to be able to log out so I can protect my account from unauthorised access.
### 2.7.4. As a returning user, <!-- omit in toc--> I'd like to be able to delete my account so I can protect my account from unauthorised access.
### 2.7.5. As a returning user, <!-- omit in toc--> I'd like to be able to report inappropriate content.

## 2.8. Responsive Design
### 2.8.1. As a returning user, <!-- omit in toc--> I’d like to browse a gallery / thumbnail view so I can engage on different levels.
### 2.8.2. As a returning user, <!-- omit in toc--> I'd like the site to be responsive so I can use it on different devices.

## 2.9. User Experience
### 2.9.1. As a returning user, <!-- omit in toc--> I want a theme that is specific, consistent and will appeal to my personal interests
### 2.9.2. As a returning user, <!-- omit in toc--> I want a visual design that is consistent and appeals to my target age group
### 2.9.3. As a returning user, <!-- omit in toc--> I'd like to see UX evokes a positive emotional response with colour, animation and sound.
### 2.9.4. As a returning user, <!-- omit in toc--> I need to be able to navigate the site comfortably so I can find content that interests me.



  
<details><summary><i>review</i></summary></details>

# 3. Automatic Testing

# 4. Issues and Bugs

## 4.2. Sign in page

“Cannot Delete ‘Forgot Password?’ On Sign in Page. Seems Completely Unresponsive to Code.” Stack Overflow, https://stackoverflow.com/questions/77427112/cannot-delete-forgot-password-on-sign-in-page-seems-completely-unresponsive. Accessed 12 Nov. 2023.

## 4.1. Google Auth Features

Issue 1: “Cannot Access Django-Admin Panel on Port.” Stack Overflow, https://stackoverflow.com/questions/77465837/cannot-access-django-admin-panel-on-port. Accessed 12 Nov. 2023.

Issue 2: “IntegrityError When Adding Social Application in Django: Null Value in Column ‘Provider_id.’” Stack Overflow, https://stackoverflow.com/questions/77466342/integrityerror-when-adding-social-application-in-django-null-value-in-column-p. Accessed 12 Nov. 2023.

# 5. Acknowledgement and credits