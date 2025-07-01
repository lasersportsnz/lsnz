// admin_grades.js: Handles editing, creating, and deleting grades in the admin UI

document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('.grades-table');
    const addBtn = document.getElementById('add-grade-btn');

    // Edit button handler
    table?.addEventListener('click', function(e) {
        if (e.target.classList.contains('edit-btn')) {
            const row = e.target.closest('tr');
            makeRowEditable(row);
        } else if (e.target.classList.contains('delete-btn')) {
            const row = e.target.closest('tr');
            if (confirm('Delete this grade?')) {
                deleteGrade(row);
            }
        } else if (e.target.classList.contains('save-btn')) {
            const row = e.target.closest('tr');
            saveGrade(row);
        } else if (e.target.classList.contains('cancel-btn')) {
            const row = e.target.closest('tr');
            cancelEdit(row);
        }
    });

    // Add new grade button
    addBtn?.addEventListener('click', function() {
        addNewGradeRow();
    });

    function makeRowEditable(row) {
        row.classList.add('editing');
        [...row.querySelectorAll('[data-field]')].forEach(td => {
            const val = td.textContent;
            if (td.dataset.field === 'description') {
                td.innerHTML = `<textarea class="form-control form-control-sm" rows="2" style="min-width:220px;max-width:100%;resize:vertical;">${val}</textarea>`;
            } else {
                td.innerHTML = `<input type="text" value="${val}" class="form-control form-control-sm">`;
            }
        });
        row.querySelector('.edit-btn').style.display = 'none';
        row.querySelector('.delete-btn').style.display = 'none';
        row.querySelector('.save-btn').style.display = '';
        row.querySelector('.cancel-btn').style.display = '';
    }

    function cancelEdit(row) {
        // Reload page to reset row (simplest for now)
        location.reload();
    }

    function saveGrade(row) {
        const id = row.dataset.id;
        const fields = {};
        row.querySelectorAll('[data-field]').forEach((td) => {
            const field = td.dataset.field;
            let value;
            if (field === 'description') {
                const textarea = td.querySelector('textarea');
                value = textarea ? textarea.value : '';
            } else {
                const input = td.querySelector('input');
                value = input ? input.value : '';
            }
            fields[field] = value;
        });
        fetch(`/admin/grades/${id ? 'update' : 'create'}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(fields)
        }).then(r => location.reload());
    }

    function deleteGrade(row) {
        const id = row.dataset.id;
        fetch(`/admin/grades/delete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id })
        }).then(r => location.reload());
    }

    function addNewGradeRow() {
        const tbody = table.querySelector('tbody');
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td data-field="letter"><input type="text" class="form-control form-control-sm"></td>
            <td data-field="points"><input type="number" class="form-control form-control-sm"></td>
            <td data-field="description"><textarea class="form-control form-control-sm" rows="2" style="min-width:220px;max-width:100%;resize:vertical;"></textarea></td>
            <td>
                <button class="btn btn-success btn-sm save-btn">Save</button>
                <button class="btn btn-secondary btn-sm cancel-btn">Cancel</button>
            </td>
        `;
        tbody.prepend(tr);
    }
});
