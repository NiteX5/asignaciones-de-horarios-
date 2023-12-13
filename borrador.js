$(document).ready(function () {
  $.ajax({
      url: '{% url "get_docents" %}',
      method: 'GET',
      dataType: 'json',
      success: function (response) {
          // Obtiene el elemento select
          var select = $('#profesorSelector');
          // Agrega las opciones desde la respuesta JSON
          response.data.forEach(function (option) {
              select.append($('<option>', {
                  value: option.id,
                  text: option.first_name + ' ' + option.last_name
              }));
          });

          // Inicializa Select2
          select.select2({
              placeholder: 'Seleccione un Docente',
              // se indica que utilizara el css de bootstrap-5
              theme: "bootstrap-5",
          });
      },
      error: function (error) {
          console.log(error);
      }

  });

  $("#profesorSelector").on('change', function () {

      idProfesor = $(this).val();
      console.log(idProfesor);

      $.ajax({
          url: '/get_subjects_assignament/' + idProfesor,
          method: 'GET',
          dataType: 'json',
          success: function (response) {
              // Obtiene el elemento select
              console.log(response.data);
              var select = $('#add-subjects');
              // Agrega las opciones desde la respuesta JSON
              response.data.forEach(function (option) {
                  select.append($('<option>', {
                      value: option.subject__id,
                      text: option.subject__subject
                  }));
              });

              // Inicializa Select2
              select.select2({
                  placeholder: 'Seleccione una Asignatura',
                  // se indica que utilizara el css de bootstrap-5
                  theme: "bootstrap-5",
                  dropdownParent: $('#modal-form'),
              });
          },
          error: function (error) {
              console.log(error);
          }

      });

      $.ajax({
          url: '/get_courses/' + idProfesor,
          method: 'GET',
          dataType: 'json',
          success: function (response) {
              // Obtiene el elemento select
              console.log(response.data);
              var select = $('#add-course');
              // Agrega las opciones desde la respuesta JSON
              response.data.forEach(function (option) {
                  select.append($('<option>', {
                      value: option.id,
                      text: option.course
                  }));
              });

              // Inicializa Select2
              select.select2({
                  placeholder: 'Seleccione una Asignatura',
                  // se indica que utilizara el css de bootstrap-5
                  theme: "bootstrap-5",
                  dropdownParent: $('#modal-form'),
              });
          },
          error: function (error) {
              console.log(error);
          }

      });

      var calendarEl = document.getElementById('calendar');
      var calendar = new FullCalendar.Calendar(calendarEl, {
          locale: 'es',
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
          editable: true,

          dateClick: function (info) {
              start = calendar.formatIso(info.date, {omitTimezoneOffset: true});
              console.log(start);
              $('#modal-form').modal('show');
              $('#btn-save-add').on('click', function() {
                  var course = document.getElementById('add-course').value;
                  var subject = document.getElementById('add-subjects').value;
                 
                  
              
                  $.ajax({
                      url: '{% url "save_schedule" %}',
                      method: 'POST',
                      data: { idPro: idProfesor, subject: subject, course: course, csrfmiddlewaretoken: '{{ csrf_token }}' },
                      dataType: 'json',
                      success: function (response) {
                          // Recarga la tabla después de agregar una asignatura
                          notyf.success(response.message);
                      },
                      error: function (error) {
                          console.log(error.responseJSON.message);
                          notyf.error(error.responseJSON.message);
                      }
                  });
              
                  // Cierra el modal de Bootstrap
                  $('#modal-form').modal('hide');
              
                  
                  });
          },
      });

      calendar.render();
  });
});



@login_required(login_url="/login/")
def get_events(request, id):
    # Obtener todos los horarios
    schedules = Schedule.objects.filter(teacher=id)
    # Serializar los datos y devolverlos como JSON
    today = datetime.today()
    prueba = ''
    data = []
    for schedule in schedules:
        id = schedule.id
        start = schedule.start.strftime("%Y-%m-%dT%H:%M:%S")
        duration = schedule.end.strftime('%H:%M')  # Asegúrate de que esto es una duración válida
        title = schedule.title
        resource = schedule.day_of_week
        extendedProps = {'course': schedule.course.course, 'subject': schedule.subject.subject, 'teacher': schedule.teacher.id}
        data.append({'id': id, 'title': title, 'start': start, 'duration': duration,'resourceId': resource , 'extendedProps': extendedProps},)
    
    return JsonResponse(data, safe=False)  # Devolver la matriz directamente