

window.onload = function() {
              nameSearchKeyUpHandler()
            };

        <!--Selectors-->
        const tableBody = document.querySelector(".table-body");
        const tableOutput = document.querySelector(".table-output");

        <!--Name Search Functionalities Start-->
        tableOutput.style.display = "none"

        const nameSearchKeyUpHandler = () =>{
            const searchValue = document.querySelector('#name-search-field').value
            console.log('searchValue', searchValue)

            tableOutput.style.display = "block";

            if(searchValue.trim().length >= 0){
                       tableBody.innerHTML = "";
                      <!--Send Data vie POST request by AJAX Start-->
                      data = {
                            searchText : searchValue,
                            csrfmiddlewaretoken : "{{csrf_token}}"
                      }

                      $.ajax({
                          type: 'POST',
                          url: '{% url "customer-list-search" %}',
                          data: data,

                          success: function (data){
                              customer_list = []
                              customer_list = data.customers
                              console.log('new data',customer_list )

                              tableOutput.style.display = "block";

                              customer_list.forEach((item) => {

                                   tableBody.innerHTML += `<tr class="infinite-item">
                                        <td>
                                            <div class="custom-control custom-checkbox">
                                                <input type="checkbox" class="custom-control-input" id="customCheck2">
                                                <label class="custom-control-label" for="customCheck2">&nbsp;</label>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="media">
                                                <img src="{% static 'assets/images/users/avatar-4.jpg' %}" alt="table-user" class="mr-3 rounded-circle avatar-sm">
                                                <div class="media-body">
                                                    <h5 class="mt-0 mb-1"><a href="javascript:void(0);" class="text-dark">{{customer.name}}</a></h5>
                                                    <p class="mb-0 font-13">${item.name}</p>
                                                </div>
                                            </div>
                                        </td>

                                        <td>${item.gender}</td>
                                        <td>${item.dob}</td>
                                        <td>${item.email}</td>
                                        <td>${item.no_of_product_purchased}</td>
                                        <td>${item.date_joined}</td>
                                        <td>
                                            <span class="badge badge-soft-success">${item.is_customer}</span>
                                        </td>

                                        <td style="width:130px">
                                            <ul class="list-inline mb-0">
                                                <li class="list-inline-item">
                                                    <a href="/user/${item.id}/detail/" class="action-icon"> <i class="mdi mdi-eye"></i></a>
                                                </li>
                                                <li class="list-inline-item">
                                                    <a href="/user/${item.id}/update/" class="action-icon"> <i class="mdi mdi-square-edit-outline"></i></a>
                                                </li>
                                                <li class="list-inline-item">
                                                    <a href="/user/${item.id}/delete/"  class="action-icon"> <i class="mdi mdi-delete"></i></a>
                                                </li>
                                            </ul>

                                        </td>
                                    </tr>`
                                })
                          }
                      })
                      <!--Send Data vie POST request by AJAX End-->

            } <!--if end-->
        } <!-- nameSearchKeyUpHandler function end-->

        <!--Name Search Functionalities End-->

        <!--Infinite Scrolling Start-->
<!--            var infinite = new Waypoint.Infinite({-->
<!--            element: $('.infinite-container')[0],-->
<!--            handler: function(direction) {-->
<!--                console.log('here',direction)-->
<!--            },-->
<!--            offset: 'bottom-in-view',-->
<!--            onBeforePageLoad: function () {-->
<!--            $('.spinner-border').show();-->
<!--            },-->
<!--            onAfterPageLoad: function () {-->
<!--            $('.spinner-border').hide();-->
<!--            }-->
<!--            });-->
        <!--Infinite Scrolling End-->