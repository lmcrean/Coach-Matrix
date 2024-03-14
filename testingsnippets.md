# testing snippets

these are currently taken out, while testing is in progress to ensure other features are fully functional with correct validation and error handling.

## Google Sign In at index.html

```html
        <form>
        <a href="{% provider_login_url 'google' %}?next=/questions/"><button type="button" class="btn -box-sd-effect" > <i class="fa fa-google fa-lg" aria-hidden="true"></i> sign in with google</button></a> 
        <!-- 
          expecting to redirect to Google Sign-in, then redirect to coachmatrix.org/questions/
          currently it redirects to http://coachmatrix.org/accounts/social/signup/
        -->
        </form>

        <hr>
        <p class="text-center">or</p>
        <hr>
```

```html
        <hr>
        <p class="text-center">or</p>
        <hr>
        
        <a href="{% provider_login_url 'google' %}?next=/questions/"><button type="button" class="btn -box-sd-effect" id="google-signup"> <i class="fa fa-google fa-lg" aria-hidden="true"></i> sign up with google</button></a>
```

## Reputation Points

currently left out of profile, as not updating as expected. Will be added to questions and answers on
- questions.html
- question_detail.html
- filtered_questions.html

place this in column 2 of question card when ready

```html
                <p class="reputation small">
                  <!--
                    reputation points, currently being tested will expand out to filtered_questions and question_detail when working. 
                    Expecting to retrieve reputation points from reputation points model
                  -->
                  <i class="fas fa-star small"></i> {{ question.author_reputation }}
                </p>
              </div>
```



