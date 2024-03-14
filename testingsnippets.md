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

## Teaching Standard Categories

currently left out of ask_questions.html, as envisioned to update as an advanced Javascript feature.

```html
        <h2 class="text-center">Category</h2>
        <label>
            Select the most Relevant <a href="https://assets.publishing.service.gov.uk/media/5a750668ed915d3c7d529cad/Teachers_standard_information.pdf" target="_blank"
            rel="noopener noreferrer">Teaching Standard</a> to your question:
        </label>
<div class="row">
                <!-- High Expectations -->
                <div class="col-6 col-sm-6 col-md-3 col-lg-3 mb-4 text-center">
                    <label class="standard-option">
                        <input type="radio" name="standard" value="1" id="high-expectations" class="d-none">
                        <div class="card">
                            <img src="https://res.cloudinary.com/dh1xovduy/image/upload/v1706366074/nrunwhqwfcbphfddo5cy.svg" class="card-img-top" alt="High Expectations">
                            <div class="card-body ">
                                <p class="card-text">High Expectations</p>
                            </div>
                        </div>
                    </label>
                </div>
                <!-- Promoting Progress -->
                <div class="col-6 col-sm-6 col-md-3 col-lg-3 mb-4 text-center">
                    <label class="standard-option">
                        <input type="radio" name="standard" value="2" id="promoting-progress" class="d-none">
                        <div class="card">
                            <img src="https://res.cloudinary.com/dh1xovduy/image/upload/v1706366075/qesqupa7ocsjjhaby877.svg" class="card-img-top" alt="Promoting Progress">
                            <div class="card-body">
                                <p class="card-text">Promoting Progress</p>
                            </div>
                        </div>
                    </label>
                </div>
                <!-- Subject Knowledge -->
                <div class="col-6 col-sm-6 col-md-3 col-lg-3 mb-4 text-center">
                    <label class="standard-option">
                        <input type="radio" name="standard" value="3" id="subject-knowledge" class="d-none">
                        <div class="card">
                            <img src="https://res.cloudinary.com/dh1xovduy/image/upload/v1706366075/ekkdgtfct1uglcjzyyff.svg" class="card-img-top" alt="Subject Knowledge">
                            <div class="card-body">
                                <p class="card-text">Subject Knowledge</p>
                            </div>
                        </div>
                    </label>
                </div>
                <!-- Planning -->
                <div class="col-6 col-sm-6 col-md-3 col-lg-3 mb-4 text-center">
                    <label class="standard-option">
                        <input type="radio" name="standard" value="4" id="planning" class="d-none">
                        <div class="card">
                            <img src="https://res.cloudinary.com/dh1xovduy/image/upload/v1706366073/phqii1p6jnleayfaicpz.svg" class="card-img-top" alt="Planning">
                            <div class="card-body">
                                <p class="card-text">Planning</p>
                            </div>
                        </div>
                    </label>
                </div>
                <!-- Differentiation -->
                <div class="col-6 col-sm-6 col-md-3 col-lg-3 mb-4 text-center">
                    <label class="standard-option">
                        <input type="radio" name="standard" value="5" id="differentiation" class="d-none">
                        <div class="card">
                            <img src="https://res.cloudinary.com/dh1xovduy/image/upload/v1706366073/adj3mwvye1kl5pmb7zdx.svg" class="card-img-top" alt="Differentiation">
                            <div class="card-body">
                                <p class="card-text">Differentiation</p>
                            </div>
                        </div>
                    </label>
                </div>
                <!-- Assessment -->
                <div class="col-6 col-sm-6 col-md-3 col-lg-3 mb-4 text-center">
                    <label class="standard-option">
                        <input type="radio" name="standard" value="6" id="assessment" class="d-none">
                        <div class="card">
                            <img src="https://res.cloudinary.com/dh1xovduy/image/upload/v1706366073/wbrndgomy1tav4zsqq5t.svg" class="card-img-top" alt="Assessment">
                            <div class="card-body">
                                <p class="card-text">Assessment</p>
                            </div>
                        </div>
                    </label>
                </div>
                <!-- Behaviour Management -->
                <div class="col-6 col-sm-6 col-md-3 col-lg-3 mb-4 text-center">
                    <label class="standard-option">
                        <input type="radio" name="standard" value="7" id="behaviour-management" class="d-none">
                        <div class="card">
                            <img src="https://res.cloudinary.com/dh1xovduy/image/upload/v1706366073/w4h6xxqceqc6adpj0g30.svg" class="card-img-top" alt="Behaviour Management">
                            <div class="card-body">
                                <p class="card-text">Behaviour Management</p>
                            </div>
                        </div>
                    </label>
                </div>
                <!-- Professionalism -->
                <div class="col-6 col-sm-6 col-md-3 col-lg-3 mb-4 text-center">
                    <label class="standard-option">
                        <input type="radio" name="standard" value="8" id="professionalism" class="d-none">
                        <div class="card">
                            <img src="https://res.cloudinary.com/dh1xovduy/image/upload/v1706366073/dbjsudz9kads8ynjywg9.svg" class="card-img-top" alt="Professionalism">
                            <div class="card-body">
                                <p class="card-text">Professionalism</p>
                            </div>
                        </div>
                    </label>
                </div>
            </div>
```

## flag feature

```html
    <!-- Flag Button -->
    <button class="btn btn-outline-warning btn-sm">
      <i class="fas fa-flag"></i> Flag
    </button>
```