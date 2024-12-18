
        // document.addEventListener('DOMContentLoaded', function() {
        //     const likeButtons = document.querySelectorAll('.like-button');
        
        //     likeButtons.forEach(button => {
        //       // Добавляем обработчик клика
        //         const questionId = button.dataset.questionId;
        //         const likeCountSpan = button.parentElement.querySelector('.like-count');
        
        
        //         fetch(`/get_like_status/${questionId}/`)
        //             .then(response => response.json())
        //             .then(data => {
        //                 if (data.liked) {
        //                  // Лайк поставлен, делаем кнопку красной
        //                  button.classList.remove('btn-outline-danger');
        //                  button.classList.add('btn-danger');
        
        //                 } else {
        //                  // Лайк снят, делаем кнопку контурной
        //                  button.classList.remove('btn-danger');
        //                  button.classList.add('btn-outline-danger');
        //                  }
        //             })
        //             .catch(error => {
        //                 console.error('Error:', error);
        //             });
        
        
        
        //       button.addEventListener('click', function() {
        //             const questionId = this.dataset.questionId;
        //             const likeCountSpan = this.parentElement.querySelector('.like-count');
        //             const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        //             fetch(`/like_question/${questionId}/`, {
        //                 method: 'POST',
        //                 headers: {
        //                     'Content-Type': 'application/json',
        //                     'X-CSRFToken': csrftoken
        //                 }
        //             })
        //             .then(response => response.json())
        //             .then(data => {
        //                 likeCountSpan.textContent = data.likes;
        //                 if (data.liked) {
        //                    // Лайк поставлен, делаем кнопку красной
        //                     button.classList.remove('btn-outline-danger');
        //                     button.classList.add('btn-danger');
        //                 } else {
        //                    // Лайк снят, делаем кнопку контурной
        //                     button.classList.remove('btn-danger');
        //                     button.classList.add('btn-outline-danger');
        //                 }
        //             })
        //             .catch(error => {
        //             console.error('Error:', error);
        //             });
        //         });
        //     });
        // });


        // document.addEventListener('DOMContentLoaded', function() {
        //     // выбираем все элементы на странице, которые имеют класс like-button
        //     const likeButtons = document.querySelectorAll('.like-button');
        
        //     // проходим по каждой кнопке лайка из likeButtons
        //     likeButtons.forEach(button => {
        //       // добавляем обработчик клика
        //       button.addEventListener('click', function() {
        //           const questionId = this.dataset.questionId; // узнаем идентификатор вопроса
        //           const likeCountSpan = this.parentElement.querySelector('.like-count'); // для обновления количества лайков после нажатия
        //           const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // получаем CSRF-токен
        
        
        //           // отправляет POST-запрос на сервер
        //           // с данными о том, что пользователь нажал на кнопку лайка
        //           fetch(`/like_question/${questionId}/`, {
        //               method: 'POST',
        //               headers: {
        //                   'Content-Type': 'application/json',
        //                   'X-CSRFToken': csrftoken
        //               }
        //           })
                      
        //               //обрабатываем ответ сервера, сервер вернет данные в формате JSON.
        //               .then(response => response.json())
        //               //обрабатываем JSON-данные, полученные от сервера
        //               .then(data => {
        //                   likeCountSpan.textContent = data.likes;
        //                   if (data.liked) {
        //                     // Лайк поставлен, делаем кнопку красной
        //                      button.classList.remove('btn-outline-danger');
        //                      button.classList.add('btn-danger');
        //                      } 

        //                    else {
        //                     // Лайк снят, делаем кнопку контурной
        //                      button.classList.remove('btn-danger');
        //                      button.classList.add('btn-outline-danger');
        //                 }
        
        //               })
        //             .catch(error => {
        //               console.error('Error:', error);
        //           });
        //         });
        //     });

        //       // добавляем обработчик при загрузке страницы
        //       // для каждой кнопки лайка, чтобы узнать, лайкнута ли запись текущим пользователем
        //       // для того, чтобы отобразить состояние кнопки “лайк” по умолчанию (лайкнут или нет) 
        //     likeButtons.forEach(button => {
        //         const questionId = button.dataset.questionId;
        //         const likeCountSpan = button.parentElement.querySelector('.like-count');
        
        //         fetch(`/get_like_status/${questionId}/`)
        //             .then(response => response.json())
        //             .then(data => {
        //                 if (data.liked) {
        //                     // Лайк поставлен, делаем кнопку красной
        //                      button.classList.remove('btn-outline-danger');
        //                      button.classList.add('btn-danger');
        //                      } 

        //                    else {
        //                     // Лайк снят, делаем кнопку контурной
        //                      button.classList.remove('btn-danger');
        //                      button.classList.add('btn-outline-danger');
        //                 }
        //             })
        //             .catch(error => {
        //                 console.error('Error:', error);
        //         });
        //     });
        // });


        document.addEventListener('DOMContentLoaded', function() {
            // Код для лайков вопросов
            const likeButtons = document.querySelectorAll('.like-button');
            likeButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const questionId = this.dataset.questionId;
                    const likeCountSpan = this.parentElement.querySelector('.like-count');
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
                    fetch(`/like_question/${questionId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            likeCountSpan.textContent = data.likes;
                            if (data.liked) {
                                button.classList.remove('btn-outline-danger');
                                button.classList.add('btn-danger');
                            } else {
                                button.classList.remove('btn-danger');
                                button.classList.add('btn-outline-danger');
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                });
            });
            likeButtons.forEach(button => {
                const questionId = button.dataset.questionId;
                fetch(`/get_like_status/${questionId}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.liked) {
                            button.classList.remove('btn-outline-danger');
                            button.classList.add('btn-danger');
                        } else {
                            button.classList.remove('btn-danger');
                            button.classList.add('btn-outline-danger');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            });
        
            // Код для лайков ответов
            const answerLikeButtons = document.querySelectorAll('.answer-like-button');
        
            answerLikeButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const answerId = this.dataset.answerId;
                    const likeCountSpan = this.parentElement.querySelector('.answer-like-count');
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        
                     fetch(`/like_answer/${answerId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        }
                     })
                    .then(response => response.json())
                    .then(data => {
                         likeCountSpan.textContent = data.likes;
                           if (data.liked) {
                            button.classList.remove('btn-outline-danger');
                            button.classList.add('btn-danger');
                        } else {
                            button.classList.remove('btn-danger');
                            button.classList.add('btn-outline-danger');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                });
            });
        
             answerLikeButtons.forEach(button => {
                const answerId = button.dataset.answerId;
                 fetch(`/get_answer_like_status/${answerId}/`)
                     .then(response => response.json())
                     .then(data => {
                         if (data.liked) {
                            button.classList.remove('btn-outline-danger');
                             button.classList.add('btn-danger');
                         } else {
                             button.classList.remove('btn-danger');
                             button.classList.add('btn-outline-danger');
                         }
                     })
                     .catch(error => {
                         console.error('Error:', error);
                     });
                 });
                 
        
            // Код для отметки правильного ответа
            const correctCheckboxes = document.querySelectorAll('.correct-answer-checkbox');
        
            correctCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    const answerId = Number(this.dataset.answerId); 
                    const questionId = Number(this.dataset.questionId);
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
                    fetch(`/set_correct_answer/${questionId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify({
                            answer_id: answerId,
                            is_correct: this.checked
                        })
        
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                // Обработка успешного ответа
                                console.log('Правильный ответ изменен!');
                                } else {
                                   // Обработка ошибки
                                   console.error('Ошибка:', data.message);
                                }
                           })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                    });
                });
        });