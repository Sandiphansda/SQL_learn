/**
 * SQL Mastery - Frontend Application
 * Handles lesson navigation, query execution, validation, and UI interactions.
 */

// ===== State =====
let lessons = { easy: [], medium: [], advanced: [] };
let currentLessonId = null;
let currentLesson = null;
let completedLessons = new Set();
let schema = {};

// ===== DOM Elements =====
const els = {
    lessonList: document.getElementById('lessonList'),
    lessonTitle: document.getElementById('lessonTitle'),
    levelBadge: document.getElementById('levelBadge'),
    lessonContent: document.getElementById('lessonContent'),
    taskBox: document.getElementById('taskBox'),
    taskText: document.getElementById('taskText'),
    sqlEditor: document.getElementById('sqlEditor'),
    resultsContent: document.getElementById('resultsContent'),
    resultsInfo: document.getElementById('resultsInfo'),
    schemaContent: document.getElementById('schemaContent'),
    progressCount: document.getElementById('progressCount'),
    progressBar: document.getElementById('progressBar'),
    prevBtn: document.getElementById('prevBtn'),
    nextBtn: document.getElementById('nextBtn'),
    hintModal: document.getElementById('hintModal'),
    hintText: document.getElementById('hintText'),
    successModal: document.getElementById('successModal'),
    successMessage: document.getElementById('successMessage'),
};

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', async () => {
    await Promise.all([loadLessons(), loadSchema(), loadProgress()]);
    renderLessonList();
    renderSchema();

    // Load first lesson if none selected
    const allLessons = getAllLessons();
    if (allLessons.length > 0 && !currentLessonId) {
        selectLesson(allLessons[0].id);
    }

    // Keyboard shortcuts
    els.sqlEditor.addEventListener('keydown', handleEditorKeydown);
});

// ===== Data Loading =====
async function loadLessons() {
    try {
        const res = await fetch('/api/lessons');
        lessons = await res.json();
    } catch (e) {
        console.error('Failed to load lessons:', e);
    }
}

async function loadSchema() {
    try {
        const res = await fetch('/api/schema');
        schema = await res.json();
    } catch (e) {
        console.error('Failed to load schema:', e);
    }
}

async function loadProgress() {
    try {
        const res = await fetch('/api/progress');
        const progress = await res.json();
        progress.forEach(id => completedLessons.add(id));
        updateProgress();
    } catch (e) {
        console.error('Failed to load progress:', e);
    }
}

// ===== Rendering =====
function getAllLessons() {
    const all = [];
    ['easy', 'medium', 'advanced'].forEach(level => {
        lessons[level].forEach(l => {
            l.level = level;
            all.push(l);
        });
    });
    return all;
}

function renderLessonList() {
    const container = els.lessonList;
    container.innerHTML = '';

    const levels = [
        { key: 'easy', label: 'Easy', icon: 'ðŸŸ¢' },
        { key: 'medium', label: 'Medium', icon: 'ðŸŸ¡' },
        { key: 'advanced', label: 'Advanced', icon: 'ðŸ”´' }
    ];

    levels.forEach(level => {
        const group = document.createElement('div');
        group.className = 'lesson-group';

        const label = document.createElement('div');
        label.className = 'group-label';
        label.textContent = `${level.icon} ${level.label}`;
        group.appendChild(label);

        lessons[level.key].forEach((lesson, idx) => {
            const item = document.createElement('div');
            item.className = 'lesson-item' + 
                (lesson.id === currentLessonId ? ' active' : '') +
                (completedLessons.has(lesson.id) ? ' completed' : '');
            item.onclick = () => selectLesson(lesson.id);

            const num = document.createElement('div');
            num.className = 'lesson-number';
            num.textContent = completedLessons.has(lesson.id) ? 'âœ“' : (idx + 1);

            const info = document.createElement('div');
            info.className = 'lesson-info';

            const name = document.createElement('div');
            name.className = 'lesson-name';
            name.textContent = lesson.title;

            const desc = document.createElement('div');
            desc.className = 'lesson-desc';
            desc.textContent = lesson.description;

            info.appendChild(name);
            info.appendChild(desc);

            const tag = document.createElement('span');
            tag.className = `level-tag tag-${level.key}`;
            tag.textContent = level.key;

            item.appendChild(num);
            item.appendChild(info);
            item.appendChild(tag);
            group.appendChild(item);
        });

        container.appendChild(group);
    });
}

function renderSchema() {
    const container = els.schemaContent;
    container.innerHTML = '';

    for (const [tableName, columns] of Object.entries(schema)) {
        const tableDiv = document.createElement('div');
        tableDiv.className = 'schema-table';

        const nameDiv = document.createElement('div');
        nameDiv.className = 'schema-table-name';
        nameDiv.textContent = tableName;
        tableDiv.appendChild(nameDiv);

        columns.forEach(col => {
            const colDiv = document.createElement('div');
            colDiv.className = 'schema-column';
            colDiv.innerHTML = `<span>${col.name}</span><span class="schema-col-type">${col.type}</span>`;
            tableDiv.appendChild(colDiv);
        });

        container.appendChild(tableDiv);
    }
}

function selectLesson(lessonId) {
    currentLessonId = lessonId;
    currentLesson = getAllLessons().find(l => l.id === lessonId);

    if (!currentLesson) return;

    // Update UI
    els.lessonTitle.textContent = currentLesson.title;
    els.levelBadge.textContent = currentLesson.level;
    els.levelBadge.className = 'level-badge ' + currentLesson.level;
    els.lessonContent.innerHTML = currentLesson.theory;
    els.taskBox.style.display = 'block';
    els.taskText.innerHTML = currentLesson.task;
    els.sqlEditor.value = '';
    els.resultsContent.innerHTML = `
        <div class="empty-state">
            <span class="empty-icon">ðŸ“Š</span>
            <p>Run a query to see results</p>
        </div>
    `;
    els.resultsInfo.textContent = '';

    // Update nav buttons
    const all = getAllLessons();
    const idx = all.findIndex(l => l.id === lessonId);
    els.prevBtn.disabled = idx === 0;
    els.nextBtn.disabled = idx === all.length - 1;
    els.prevBtn.style.opacity = idx === 0 ? '0.4' : '1';
    els.nextBtn.style.opacity = idx === all.length - 1 ? '0.4' : '1';

    renderLessonList();

    // Highlight relevant tables in schema
    highlightSchemaTables(currentLesson.tables || []);
}

function highlightSchemaTables(tableNames) {
    const tables = document.querySelectorAll('.schema-table');
    tables.forEach(table => {
        const name = table.querySelector('.schema-table-name').textContent;
        if (tableNames.includes(name)) {
            table.style.borderColor = 'var(--accent-blue)';
            table.style.boxShadow = '0 0 0 1px var(--accent-blue)';
        } else {
            table.style.borderColor = '';
            table.style.boxShadow = '';
        }
    });
}

function updateProgress() {
    const total = getAllLessons().length;
    const completed = completedLessons.size;
    els.progressCount.textContent = completed;
    els.progressBar.style.width = total > 0 ? `${(completed / total) * 100}%` : '0%';
}

// ===== Navigation =====
function prevLesson() {
    const all = getAllLessons();
    const idx = all.findIndex(l => l.id === currentLessonId);
    if (idx > 0) selectLesson(all[idx - 1].id);
}

function nextLesson() {
    const all = getAllLessons();
    const idx = all.findIndex(l => l.id === currentLessonId);
    if (idx < all.length - 1) selectLesson(all[idx + 1].id);
}

// ===== Query Execution =====
async function runQuery() {
    const query = els.sqlEditor.value.trim();
    if (!query) {
        showError('Please enter a SQL query');
        return;
    }

    showLoading();

    try {
        const res = await fetch('/api/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        const data = await res.json();

        if (data.error) {
            showError(data.error);
        } else {
            showResults(data.columns, data.rows);
        }
    } catch (e) {
        showError('Network error: ' + e.message);
    }
}

async function validateSolution() {
    if (!currentLesson) return;

    const query = els.sqlEditor.value.trim();
    if (!query) {
        showError('Please write a query first');
        return;
    }

    showLoading();

    try {
        const res = await fetch('/api/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lesson_id: currentLessonId, query })
        });
        const data = await res.json();

        if (data.columns && data.rows) {
            showResults(data.columns, data.rows);
        }

        if (data.correct) {
            completedLessons.add(currentLessonId);
            updateProgress();
            renderLessonList();
            showSuccess(data.message);
        } else {
            showError(data.message);
        }
    } catch (e) {
        showError('Validation error: ' + e.message);
    }
}

// ===== UI Helpers =====
function showResults(columns, rows) {
    els.resultsInfo.textContent = `${rows.length} row${rows.length !== 1 ? 's' : ''}`;

    if (rows.length === 0) {
        els.resultsContent.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">ðŸ“­</span>
                <p>Query returned 0 rows</p>
            </div>
        `;
        return;
    }

    const table = document.createElement('table');
    table.className = 'data-table';

    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    rows.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            const val = row[col];
            td.textContent = val !== null && val !== undefined ? val : 'NULL';
            if (val === null || val === undefined) {
                td.style.color = 'var(--text-muted)';
                td.style.fontStyle = 'italic';
            }
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    els.resultsContent.innerHTML = '';
    els.resultsContent.appendChild(table);
}

function showError(message) {
    els.resultsContent.innerHTML = `
        <div class="message message-error">
            <span>âš ï¸</span> ${escapeHtml(message)}
        </div>
    `;
    els.resultsInfo.textContent = 'Error';
}

function showSuccess(message) {
    els.successMessage.textContent = message;
    els.successModal.classList.add('active');
}

function showLoading() {
    els.resultsContent.innerHTML = `
        <div class="empty-state">
            <span class="empty-icon">â³</span>
            <p>Running query...</p>
        </div>
    `;
}

function resetEditor() {
    els.sqlEditor.value = '';
    els.resultsContent.innerHTML = `
        <div class="empty-state">
            <span class="empty-icon">ðŸ“Š</span>
            <p>Run a query to see results</p>
        </div>
    `;
    els.resultsInfo.textContent = '';
}

function showHint() {
    if (!currentLesson) return;
    els.hintText.textContent = currentLesson.hint;
    els.hintModal.classList.add('active');
}

function closeHint() {
    els.hintModal.classList.remove('active');
}

function showSolution() {
    if (!currentLesson) return;
    if (confirm('Are you sure you want to see the answer? Try solving it yourself first!')) {
        els.sqlEditor.value = currentLesson.solution;
    }
}

function closeSuccess() {
    els.successModal.classList.remove('active');
    // Auto-advance to next lesson
    const all = getAllLessons();
    const idx = all.findIndex(l => l.id === currentLessonId);
    if (idx < all.length - 1) {
        nextLesson();
    }
}

// ===== Keyboard Shortcuts =====
function handleEditorKeydown(e) {
    // Ctrl/Cmd + Enter to run
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        runQuery();
    }
    // Tab to insert spaces
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = els.sqlEditor.selectionStart;
        const end = els.sqlEditor.selectionEnd;
        els.sqlEditor.value = els.sqlEditor.value.substring(0, start) + '    ' + els.sqlEditor.value.substring(end);
        els.sqlEditor.selectionStart = els.sqlEditor.selectionEnd = start + 4;
    }
}

// ===== Utility =====
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Close modals on backdrop click
window.onclick = function(e) {
    if (e.target === els.hintModal) closeHint();
    if (e.target === els.successModal) closeSuccess();
};
