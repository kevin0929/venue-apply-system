$(document).ready(function() {
    $('#datepicker').datepicker({
        format: 'yyyy-mm',
        autoclose: true,
        todayHighlight: true,
        language: 'zh-TW'
    }).on('changeDate', function(e) {
        generateCalendar(e.date);
    });

    function generateCalendar(date) {
        var daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
        var firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
        var calendar = $('#calendar');
        calendar.empty();

        for (var i = 0; i < firstDay; i++) {
            calendar.append('<div class="day"></div>');
        }

        for (var day = 1; day <= daysInMonth; day++) {
            var dayDate = new Date(date.getFullYear(), date.getMonth(), day);
            var formattedDate = dayDate.toISOString().split('T')[0];
            calendar.append('<div class="day" data-date="' + formattedDate + '" data-toggle="modal" data-target="#bookingModal">' + day + '</div>');
        }
    }
    generateCalendar(new Date());

    $('#reserve').click(function() {
        console.log(bookUrl);
        $.ajax({
            type: "POST",
            url: bookUrl,
            success: function(response) {
                alert('success');
            },
            error: function(xhr, status, error) {
                alert('failed: ' + error);
            }
        });
    });
});
