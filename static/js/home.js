
if ($(window).width() < 1024) {
  $("#nav-menu").slideUp(0);
}

$("#menu-toggle").on("click", function () {
  if ($(window).width() < 1024) {
    $("#nav-menu").slideToggle("slow");
  }
});

$(window).resize(function () {
  if ($(window).width() >= 1024) {
    $("#nav-menu").show();
  } else {
    $("#nav-menu").hide();
  }
});

$("#datepickerend, #datepickerstart").datepicker();

$("#searchButton").click(function () {
  fetchTask(create_search_url(url, getFilterSearchValue));
});

$("#fiterandsortButton").click(function () {
  fetchTask(create_search_url(url, getFilterValue));
});

let url = "/api/";
let lastUrl = url;

// get the filter values from the dom
function getFilterSearchValue() {
  const searchValue = $("#search_task").val();
  const selectedPriority = $("input[name='priority_radio']:checked").val();
  const selectedStatus = $("input[name='status_radio']:checked").val();
  const selectedCategory = $("input[name='category_radio']:checked").val();
  const selectedSortBy = $("input[name='sort_radio']:checked").val();
  const start_date = $("#datepickerstart").val();
  const end_date = $("#datepickerend").val();

  return {
    query: searchValue,
    priority: selectedPriority,
    status: selectedStatus,
    category: selectedCategory,
    start_date: start_date,
    end_date: end_date,
    sort_by: selectedSortBy,
  };
}

function getFilterValue() {
  const values = getFilterSearchValue();
  const newValues = { ...values, query: "" };
  return newValues;
}

//create the url with the query params
function create_search_url(url, filterValues) {
  const filters = filterValues();
  let queryParams = [];

  // Iterate through filters and add non-empty values to queryParams
  for (const key in filters) {
    if (filters[key]) {
      queryParams.push(`${key}=${encodeURIComponent(filters[key])}`);
    }
  }

  // Construct the final URL with query parameters
  if (queryParams.length > 0) {
    const queryString = queryParams.join("&");
    return `${url}?${queryString}`;
  } else {
    return url;
  }
}

// Define the async function to send HTTP requests
async function SendHttpRequest(method, url, data = null) {
  try {
    // Use a Promise to wrap jQuery's AJAX call
    return new Promise((resolve, reject) => {
      $.ajax({
        url: url,
        method: method.toUpperCase(),
        headers: {
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        dataType: "json",
        contentType: "application/json",
        data: data ? JSON.stringify(data) : null,
        success: function (data) {
          resolve(data); // Resolve the Promise with the received data
        },
        error: function (jqXHR, textStatus, errorThrown) {
          let errorMessage = errorThrown || textStatus;
          if (jqXHR.responseJSON) {
            errorMessage = jqXHR.responseJSON; // Use the responseText as error message if available
          }
          reject(jqXHR); // Reject the Promise with the error message
        },
      });
    });
  } catch (error) {
    throw new Error(`Error fetching data: ${error}`);
  }
}

// Example usage within an async function
async function fetchTask(url, addcard = true) {
  try {
    const method = "GET";
    const searchUrl = url;
    lastUrl = searchUrl;

    const responseData = await SendHttpRequest(method, searchUrl);
    const { inProgressTasks, completedTasks, overdueTasks } =
      filterData(responseData);
    loadTasks(
      inProgressTasks,
      "in_progress_tasks",
      "No Task In progress",
      "in_progress_count_con",
      addcard
    );
    loadTasks(
      completedTasks,
      "completed_tasks_con",
      "No Completed Task",
      "completed_counnt_con",
      addcard
    );
    loadTasks(
      overdueTasks,
      "overdue_task_con",
      "No Over Dued Task",
      "overdue_count_con",
      addcard
    );
    // $(".sortable-list").sortable( "refresh" );
  } catch (e) {
    const error = e.responseJSON;
    error.forEach((err) => {
      iziToast.error({
        message: err,
        position: "topCenter",
        class: "fixed top-20",
      });
    });
  }
}

function loadTasks(
  tasksData,
  id,
  emptyMessage,
  countConId,
  addcard = true
) {
  const $taskListContainer = $(`#${id}`);
  const $taskCountContainer = $(`#${countConId}`);

  $taskCountContainer.empty();

  $taskCountContainer.text(`(${tasksData.length})`);

  if (addcard) {
    $taskListContainer.empty();
    $.each(tasksData, function (index, task) {
      // Create elements to display task information
      const $taskElement = $(
        `<div data-task-id=${task.id} class="handle"></div>`
      );
      $taskElement.html(`
    <div class="mt-10" >
        <div class="flex gap-5 mb-2.5">
          <span class="text-xs text-gray-500 py-1 px-3 rounded  shadow-lg ${priorityColor(
            task.priority
          )}"
            >${task.priority}</span
          >
          <span class="text-xs text-purple-500 py-1 px-3 rounded shadow-lg"
            ><i class="far fa-clock me-2"></i>${
              task.formatted_due_date
            }</span
          >
          <span
            class="text-xs bg-purple-100 text-purple-500 py-1 px-3 rounded  shadow-lg"
            >${titleCase(task.category)}</span
          >
        </div>
        <div class="bg-darkGray p-4 rounded shadow-md mb-4 flex flex-col h-[150px] justify-between py-2">
         <div>
          <h3 class="font-semibold mb-2">${titleCase(task.title)}</h3>
          <p class="text-sm text-gray-600 mb-4">
            ${truncateChars(task.description, 100)}
          </p>
         </div>
         <div class="">
          <div class="flex items-center justify-between ">        
          <div class="text-[8px] bg-[#374151] p-1 shadow rounded text-white">
              ${task.assigned_to.username}
          </div>
          ${otherBtn(task)}
            </div>
         </div>
        </div>
      </div>
    `);
      $taskListContainer.append($taskElement);
    });
  }

  function otherBtn(task) {
    if (task.owner) {
        return (` <div class="flex space-x-2">
            <button class="text-gray-400 hover:text-gray-600 task_deleter" data-id="${task.id}">
                <i class="fas fa-trash-alt"></i>
            </button>
            <button class="text-gray-400 hover:text-gray-600 task_editer" data-id="${task.id}">
                <i class="fas fa-edit"></i>
            </button>
          </div>`);
    }
    return "";
}
  // show no task massage
  // if (!tasksData.length){
  //     $taskListContainer.append(`
  //     <div class="flex justify-center bg-darkGray text-sm rounded mt-10">
  //         <p class="text-sm">${emptyMessage}</p>
  //     </div>
  //     `)
  // }
}

function priorityColor(value) {
  const colorMap = {
    high: "bg-red-100",
    medium: "bg-darkGray",
    low: "bg-green-100",
  };
  return colorMap[value.toLowerCase()] || "bg-red-100";
}

function titleCase(str) {
  return str
    .toLowerCase()
    .split(" ")
    .map(function (word) {
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}

function truncateChars(str, maxChars) {
  if (str.length <= maxChars) {
    return str;
  }
  return str.slice(0, maxChars) + "...";
}

function filterData(taskData) {
  const inProgressTasks = taskData.filter(
    (task) => task.status.toLowerCase() === "in progress"
  );
  const completedTasks = taskData.filter(
    (task) => task.status.toLowerCase() === "completed"
  );
  const overdueTasks = taskData.filter(
    (task) => task.status.toLowerCase() === "overdue"
  );

  return { inProgressTasks, completedTasks, overdueTasks };
}

//----------------------- sorting and dragging----------
let isSortingCancelled = false;
$(".sortable-list")
  .sortable({
    connectWith: ".sortable-list",
    dropOnEmpty: true,
    stop: function (event, ui) {
      handleUpdateEvent(event, ui);
    },
  })
  .disableSelection();

async function handleUpdateEvent(event, ui) {
  const itemId = ui.item.attr("data-task-id");
  const columnName = ui.item.parent().attr("data-column");
  try {
    const data = { status: columnName };
    const url = `/api/${itemId}/`;
    const responseData = await SendHttpRequest("PATCH", url, data);
    fetchTask(lastUrl, false);
  } catch (e) {
    const status = e.status;
    $(".sortable-list").sortable("cancel");
    if (status == 403) {
      iziToast.warning({
        message: "You cannot update status of task not assigned to you",
        position: "topCenter",
        class: "fixed top-20",
        timeout: 2000,
      });
    } else {
      iziToast.error({
        message: "Login to update status of task",
        position: "topCenter",
        class: "fixed top-20",
        timeout: 2000,
      });
    }
  }
}

// ---------------------------------------  Modal Actions ----------------------------------------

const $addTaskBtn = $("#add-task-btn");
const $taskModal = $("#task-modal");
const $closeModal = $("#close-modal");
const $taskSubmitBtn = $("#task-submit");



function initializeModalInputs() {
  const $taskNameInput = $("#task-name");
  const $taskCategoryInput = $("#task-category");
  const $taskUserInput = $("#task-user");
  const $taskDetailsTextarea = $("#task-details");
  const $taskStatusSelect = $("#task-status");
  const $taskPrioritySelect = $("#task-priority");
  const $dueDateInput = $("#due_date");

  return {
    $taskNameInput: $taskNameInput,
    $taskCategoryInput: $taskCategoryInput,
    $taskUserInput: $taskUserInput,
    $taskDetailsTextarea: $taskDetailsTextarea,
    $taskStatusSelect: $taskStatusSelect,
    $taskPrioritySelect: $taskPrioritySelect,
    $dueDateInput: $dueDateInput,
  };
}

function clearModalInputs(inputs) {
  inputs.$taskNameInput.val('');
  inputs.$taskCategoryInput.val('');
  inputs.$taskUserInput.val('');
  inputs.$taskDetailsTextarea.val('');
  inputs.$taskStatusSelect.val('');
  inputs.$taskPrioritySelect.val('');
  inputs.$dueDateInput.val('');
}

function mapFormData() {
  const modalInputs = initializeModalInputs(); // Get modal inputs

  // Extract values using .val() and map to form data object
  const formData = {
    title: modalInputs.$taskNameInput.val(),
    description: modalInputs.$taskDetailsTextarea.val(),
    status: modalInputs.$taskStatusSelect.val(),
    priority: modalInputs.$taskPrioritySelect.val(),
    due_date: modalInputs.$dueDateInput.val(),
    category: modalInputs.$taskCategoryInput.val(), 
    assigned_to: modalInputs.$taskUserInput.val(),
  };

  return formData;
}

$taskSubmitBtn.click(async function (e) {
  e.preventDefault();
  const formData = mapFormData();
  const url = "/api/"
  try{
    const response = await SendHttpRequest("POST",url, formData)
    fetchTask(lastUrl,true)
    const inputs = initializeModalInputs();
    clearModalInputs(inputs);
    $taskModal.addClass("hidden");
    iziToast.success({
      message: "Task created successfully",
      position: "topCenter",
      class: "fixed top-20",
      timeout: 3000,
  });

  }
  catch(e){
    errors = e.responseJSON
    displayErrors(errors);
  }
});

function displayErrors(errors) {
  for (const [title, messages] of Object.entries(errors)) {
      messages.forEach(message => {
          iziToast.error({
              title: title.charAt(0).toUpperCase() + title.slice(1),
              message: "This field isn't Valid",
              position: "topRight",
              class: "fixed top-20",
              timeout: 5000,
          });
      });
  }
}

$addTaskBtn.on("click", function () {
  $taskModal.removeClass("hidden");
});

$closeModal.on("click", function () {
  $taskModal.addClass("hidden");
});

$(window).on("click", function (event) {
  if ($(event.target).is($taskModal)) {
    $taskModal.addClass("hidden");
    
  }
});




const $deleteModal = $("#delete-modal");
const $closeDeleteModal = $("#close-delete-modal");
const $submitDeleteModal = $("#delete-submit-modal");

$(window).on('click', function(event) {
  if ($(event.target).is($deleteModal)) {
      $deleteModal.addClass("hidden");
  }
});


$(document).on('click', '.task_deleter', function(event) {
  const taskId = $(this).data('id');
  $deleteModal.removeClass("hidden")
  $submitDeleteModal.attr('data-id', taskId);
});

$submitDeleteModal.on('click',async function() {
const taskId = $submitDeleteModal.attr("data-id")
const url = `/api/${taskId}/`
const response = await SendHttpRequest("DELETE",url)
fetchTask(lastUrl,true)
$deleteModal.addClass("hidden")
iziToast.success({
  message: "Task deleted successfully",
  position: "topCenter",
  class: "fixed top-20",
  timeout: 3000,
});

})

$closeDeleteModal.on("click",function(){
$deleteModal.addClass("hidden")
})


// Edit modal
const $addTaskBtn2 = $("#add-task-btn2");
const $taskModal2 = $("#task-modal2");
const $closeModal2 = $("#close-modal2");
const $taskSubmitBtn2 = $("#task-submit2");

$(window).on("click", function (event) {
if ($(event.target).is($taskModal2)) {
  $taskModal2.addClass("hidden");
  
}
});

$(document).on('click', '.task_editer',async function(event) {
const taskId = $(this).data('id');
const url = `/api/${taskId}/`
const response = await SendHttpRequest("GET",url)
$taskModal2.attr("data-task-id",taskId)
const {
  $taskNameInput,
  $taskCategoryInput,
  $taskUserInput,
  $taskDetailsTextarea,
  $taskStatusSelect,
  $taskPrioritySelect,
  $dueDateInput,
} = initializeModalInputs2()
$taskNameInput.val(response.title)
$taskCategoryInput.val(response.category)
$taskUserInput.val(response.assigned_to.id)
$taskDetailsTextarea.val(response.description)
$taskStatusSelect.val(response.status)
$taskPrioritySelect.val(response.priority)
$dueDateInput.val(getDateOnly(response.due_date))

$taskModal2.removeClass("hidden")
});

function getDateOnly(isoDateString, locale = 'en-CA', options = { year: 'numeric', month: '2-digit', day: '2-digit' }) {
const dateObject = new Date(isoDateString);
// Extract only the date part with custom formatting options
return dateObject.toLocaleDateString(locale, options);
}

function initializeModalInputs2() {
const $taskNameInput = $("#task-name2");
const $taskCategoryInput = $("#task-category2");
const $taskUserInput = $("#task-user2");
const $taskDetailsTextarea = $("#task-details2");
const $taskStatusSelect = $("#task-status2");
const $taskPrioritySelect = $("#task-priority2");
const $dueDateInput = $("#due_date2");

return {
  $taskNameInput: $taskNameInput,
  $taskCategoryInput: $taskCategoryInput,
  $taskUserInput: $taskUserInput,
  $taskDetailsTextarea: $taskDetailsTextarea,
  $taskStatusSelect: $taskStatusSelect,
  $taskPrioritySelect: $taskPrioritySelect,
  $dueDateInput: $dueDateInput,
};
}

function clearModalInputs2(inputs) {
inputs.$taskNameInput.val('');
inputs.$taskCategoryInput.val('');
inputs.$taskUserInput.val('');
inputs.$taskDetailsTextarea.val('');
inputs.$taskStatusSelect.val('');
inputs.$taskPrioritySelect.val('');
inputs.$dueDateInput.val('');
}

function mapFormData2() {
const modalInputs = initializeModalInputs2(); // Get modal inputs

// Extract values using .val() and map to form data object
const formData = {
  title: modalInputs.$taskNameInput.val(),
  description: modalInputs.$taskDetailsTextarea.val(),
  status: modalInputs.$taskStatusSelect.val(),
  priority: modalInputs.$taskPrioritySelect.val(),
  due_date: modalInputs.$dueDateInput.val(),
  category: modalInputs.$taskCategoryInput.val(), 
  assigned_to: modalInputs.$taskUserInput.val(),
};

return formData;
}

$taskSubmitBtn2.click(async function (e) {
e.preventDefault();
const formData = mapFormData2();
const taskId = $taskModal2.attr("data-task-id")
const url = `/api/${taskId}/`
try{
  const response = await SendHttpRequest("PUT",url, formData)
  fetchTask(lastUrl,true)
  const inputs = initializeModalInputs2();
  clearModalInputs(inputs);
  $taskModal2.addClass("hidden");
  iziToast.success({
    message: "Task Update successfully",
    position: "topCenter",
    class: "fixed top-20",
    timeout: 3000,
});

}
catch(e){
  errors = e.responseJSON
  displayErrors(errors);
}
});

function displayErrors(errors) {
for (const [title, messages] of Object.entries(errors)) {
    messages.forEach(message => {
        iziToast.error({
            title: title.charAt(0).toUpperCase() + title.slice(1),
            message: "This field isn't Valid",
            position: "topRight",
            class: "fixed top-20",
            timeout: 5000,
        });
    });
}
}

$addTaskBtn.on("click", function () {
$taskModal.removeClass("hidden");
});

$closeModal.on("click", function () {
$taskModal.addClass("hidden");
});

$(window).on("click", function (event) {
if ($(event.target).is($taskModal)) {
  $taskModal.addClass("hidden");
  
}
});2  
