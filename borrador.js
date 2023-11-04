
  
  document.addEventListener("DOMContentLoaded", function () {
    var containerEl = document.getElementById("external-events-list");
    var calendarEl = document.getElementById("kt_docs_fullcalendar_drag");
    var calendar = null;

    // Hacer una solicitud Ajax para obtener los eventos
    $.get('/get_subjects/', function (data) {
        var events = data.data;

        events.forEach(function (event) {
            var title = event.subject + " - " + event.course__course;
            var eventId = event.id;
            var courseId = event.course__id;
            var duration = "00:45";

            // Crear un elemento de evento
            var eventItem = document.createElement('div');
            eventItem.className = "fc-event draggable-event";
            eventItem.setAttribute("data-event", JSON.stringify({
                title: title,
                duration: duration,
                courseId: courseId,
                eventId: eventId
            }));

            var eventText = document.createElement('p');
            eventText.className = "list-group-item list-group-item-action";
            eventText.textContent = title;

            eventItem.appendChild(eventText);
            containerEl.appendChild(eventItem);

            // Inicializar FullCalendar Draggable después de cargar los eventos
            new FullCalendar.Draggable(eventItem, {
                eventData: function (eventEl) {
                    var json_event = eventEl.getAttribute("data-event");
                    var event_array = JSON.parse(json_event);
                    var duration = "00:45";
                    var event_title = event_array.title;
                    return {
                        title: event_title,
                        duration: duration,
                        courseId: event_array.courseId,
                        eventId: event_array.eventId
                    };
                },
            });
        });

        // Inicializar FullCalendar una vez que se hayan cargado los eventos
        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: "timeGridWeek",
            headerToolbar: false,
            droppable: true,
            selectable: true,
            editable: true,
            allDaySlot: false,
            slotMinTime: "08:00:00",
            slotMaxTime: "18:00:00",
            slotDuration: "00:15",
            slotLabelInterval: "00:15",
            eventOverlap: false,
            contentHeight: 'auto',
            hiddenDays: [0, 6],
            editable: true, // Permite mover eventos
            drop: function (arg) {
                // Elimina el evento del calendario
                arg.draggedEl.remove();
            },
        });

        calendar.setOption('height', 250);
        calendar.render();
    });
});