const frame180   = document.getElementById('Frame180');
const editBtn    = document.getElementById('edit-btn');
const selectAllRow = document.getElementById('select-all-row');
const selectAll  = document.getElementById('select-all');
const checkboxes = document.querySelectorAll('.record-checkbox');
const deleteForm = document.getElementById('delete-form');

let isEditMode = false;

function getCheckedCount() {
    return document.querySelectorAll('.record-checkbox:checked').length;
}

function updateEditBtn() {
    if (!isEditMode) return;
    if (getCheckedCount() > 0) {
        editBtn.textContent = '삭제';
        editBtn.classList.add('delete-mode');
    } else {
        editBtn.textContent = '완료';
        editBtn.classList.remove('delete-mode');
    }
}

function enterEditMode() {
    isEditMode = true;
    frame180.classList.add('edit-mode');
    selectAllRow.style.display = 'flex';
    editBtn.textContent = '완료';
    editBtn.classList.remove('delete-mode');
}

function exitEditMode() {
    isEditMode = false;
    frame180.classList.remove('edit-mode');
    selectAllRow.style.display = 'none';
    editBtn.textContent = '편집';
    editBtn.classList.remove('delete-mode');
    checkboxes.forEach(cb => cb.checked = false);
    selectAll.checked = false;
}

editBtn.addEventListener('click', function () {
    if (!isEditMode) {
        enterEditMode();
    } else if (getCheckedCount() > 0) {
        deleteForm.submit();
    } else {
        exitEditMode();
    }
});

checkboxes.forEach(cb => {
    cb.addEventListener('change', function () {
        selectAll.checked = getCheckedCount() === checkboxes.length;
        updateEditBtn();
    });
});

selectAll.addEventListener('change', function () {
    checkboxes.forEach(cb => cb.checked = this.checked);
    updateEditBtn();
});
