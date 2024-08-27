$(document).ready(function() {
    function generateCalendar(date, applications) {
        var daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
        var firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
        var calendar = $('#calendar');
        calendar.empty();
    
        for (var i = 0; i < firstDay; i++) {
            calendar.append('<div class="day"></div>');
        }
    
        for (var day = 1; day <= daysInMonth; day++) {
            var dayDate = new Date(date.getFullYear(), date.getMonth(), day);
            var formattedDate = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + day;
    
            var dayApplications = applications.filter(app => (app.date == formattedDate && app.venue_id == venueid));
    
            if (dayApplications.length > 0) {
                var content = day + '<br>';
                dayApplications.forEach(application => {
                    content += '<small>' + application.user + '</small><br>';
                });
    
                calendar.append('<div class="day reserved" data-date="' + formattedDate + '" data-toggle="modal" data-target="#bookingModal">' +
                    content + '</div>');
            } else {
                calendar.append('<div class="day" data-date="' + formattedDate + '" data-toggle="modal" data-target="#bookingModal">' + day + '</div>');
            }
        }
    }

    function loadApplicationsAndGenerateCalendar(date) {
        $.ajax({
            url: venueUrl,
            type: 'GET',
            success: function(applications) {
                generateCalendar(date, applications);
            },
            error: function(error) {
                console.log('Failed to load reservations: ', error);
            }
        });
    }

    $('#datepicker').datepicker({
        format: 'yyyy-mm',
        autoclose: true,
        todayHighlight: true,
        language: 'zh-TW',
        minViewMode: 1
    }).on('changeDate', function(e) {
        loadApplicationsAndGenerateCalendar(e.date);
    });

    $('#reserve').click(function() {
        $.ajax({
            type: "POST",
            url: applyUrl,
            success: function(response) {
                alert('success to apply!');
                window.location.reload();
            },
            error: function(xhr, status, error) {
                alert('failed: ' + error);
            }
        });
    });

    $('#cancel').click(function() {
        $.ajax({
            type: "POST",
            url: deleteUrl,
            success: function(response) {
                alert('success to delete!');
                window.location.reload();
            },
            error: function(xhr, status, error) {
                alert('failed: ' + error);
            }
        })
    })

    $('#queue').click(function() {
        $.ajax({
            type: "POST",
            url: queueUrl,
            success: function(response) {
                alert('success to queue!');
                window.location.reload();
            },
            error: function(xhr, status, error) {
                alert('failed: ' + error);
            }
        })
    })

    function formatDate(date) {
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        return year + '-' + ('0' + month).slice(-2);
    }
});
