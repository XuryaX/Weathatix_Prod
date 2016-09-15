/**
 * Created by shaur on 28-08-2016.
 */

$(document).ready(function(){

    google.charts.load('current', {packages: ['corechart','line']});
    (function (){
        $.ajax({
            url : "/api/country-list/",
            complete: function(data){
                var country_list = JSON.parse(data.responseText);
                for (country_index in country_list){
                    country = country_list[country_index];
                    $('#country').append($('<option>',
                         {
                            value: country,
                            text : country
                        }));

                }
            }

        })

    }());

    $('#country').on('change',function(evt){
       country = $(this).find(":selected").text();

        $.ajax({
            url : "/api/city-list/"+country,
            complete: function(data){
                var city_list = JSON.parse(data.responseText);
                for (city_index in city_list){
                    city = city_list[city_index];
                    $('#city').append($('<option>',
                         {
                            value: city,
                            text : city
                        }));

                }
            }

        })
    });

    $('#city').on('change',function(evt){
       city = $(this).find(":selected").text();
        country = $("#country").find(":selected").text();

        $.ajax({
            url : "/api/station-list/"+country+"/"+city,
            complete: function(data){
                var station_json = JSON.parse(data.responseText).station;

                for (station_object in station_json){
                    value = station_json[station_object].id;
                    text = station_json[station_object].neighborhood;
                    $('#station').append($('<option>',
                    {
                        value: value,
                        text : text
                    }));
                }
            }

        })
    });


    $("#modal_close").on('click',function(){
        $("#email_modal").hide(300)
    });

    $("#schedule_link").on('click',function(){
        $("#email_modal").css({"display":"block"});
        $("#email_modal").show(300)
    });

    function before_ajax_setcsrf(xhr, settings){
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                         var cookies = document.cookie.split(';');
                         for (var i = 0; i < cookies.length; i++) {
                             var cookie = jQuery.trim(cookies[i]);
                             // Does this cookie string begin with the name we want?
                             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                 break;
                             }
                         }
                     }
                     return cookieValue;
                 }
                 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                     // Only send the token to relative URLs i.e. locally.
                     xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                 }

    }

    $("#schedule").on('click',function(){
        var data = {};
        data.station_id = $("#schedule_station").find(":selected").val();
        $.ajax({
            url: '/subscribe',
            beforeSend: before_ajax_setcsrf,
            contentType: "application/json",
            data:JSON.stringify(data),
            type: 'PUT',
            success: function(result) {
                if(result=="Registered"){
                    alert("You have already subscribed");
                }
                $("#email_modal").hide(300)
            }
        });
    });

    $("#add_station").on("click",function(){
        var text = $("#station").find(":selected").text();
        var value = $("#station").find(":selected").val();

        var data = {};
        data.station_id = value;
        data.area = text;
        $.ajax({
            url: '/add_station',
            beforeSend: before_ajax_setcsrf,
            type: 'PUT',
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function(result) {
                if(result=="Registered"){
                    alert("You have already added this station");
                }
                else {
                    $('#stations').append($('<option>',
                        {
                            value: value,
                            text: text
                        }));
                    $('#schedule_station').append($('<option>',
                        {
                            value: value,
                            text: text
                        }));
                }
            }
        });

    });



    $("#plot_btn").on('click', function () {
        google.charts.setOnLoadCallback(drawChart);
        function drawChart() {


            var param = $(('[name="parameter"]:checked')).val();
            var start = $(('#start')).val();
            var end = $(('#end')).val();
            var data;
            var station = $(('#stations')).val();

            start = new Date(start).getTime() / 1000;
            end = new Date(end).getTime() / 1000;

            var isValid = true;
            var msg;
            if(!param){
                isValid = false;
                msg = "Parameter is required";
            }
            if(!station){
                isValid = false;
                msg = "Station is required";
            }

            if (!end || ! start){
                isValid = false;
                msg = "Please Select Date Range";
            }
            if(end<start){
                isValid = false;
                msg = "End Date cannot be less than start date";
            }
            if(isValid){

                $("#load").show(300);
                $.ajax({
                    url: "/api/daily-forecast/" + station + "/" + start + "/" + end,
                    complete: function (data) {
                        var query_resp = JSON.parse(data.responseText);
                        data = new Array();
                        $.each(query_resp,function(index,value){
                            var paramValue;
                            var paramDate;
                            if(param==="Temperature"){
                                paramValue = parseFloat(value.high.celsius);
                            }
                            else{
                                paramValue = parseFloat(value.avehumidity);
                            }
                            paramDate = new Date(value.date.epoch*1000);

                            data.push([paramDate,paramValue]);

                        });

                        var data_table = new google.visualization.DataTable();
                        data_table.addColumn('date', 'Range');
                        data_table.addColumn('number', param);
                        data_table.addRows(data);

                        // Instantiate and draw the chart.
                        var chart = new google.visualization.LineChart(document.getElementById('graph'));
                        chart.draw(data_table, null);
                        $("#load").hide(300);
                    }
                });
            }
            else{
                alert(msg);
            }
        }
    });
});