document.getElementById('fileInput').addEventListener('change', handleFileSelect, false);
document.getElementById('templateInput').addEventListener('change', handleTemplateSelect, false);

let jsonData = {};
let templates = {};

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                jsonData = JSON.parse(e.target.result);
                console.log('JSON data parsed successfully:', jsonData);
                renderTable();
            } catch (err) {
                alert('Error parsing JSON file: ' + err.message);
                console.error('Error parsing JSON file:', err);
            }
        };
        reader.onerror = function(err) {
            alert('Error reading file: ' + err.message);
            console.error('Error reading file:', err);
        };
        reader.readAsText(file);
    } else {
        alert('No file selected.');
    }
}

function handleTemplateSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                templates = JSON.parse(e.target.result);
                console.log('Template data parsed successfully:', templates);
            } catch (err) {
                alert('Error parsing template file: ' + err.message);
                console.error('Error parsing template file:', err);
            }
        };
        reader.onerror = function(err) {
            alert('Error reading template file: ' + err.message);
            console.error('Error reading template file:', err);
        };
        reader.readAsText(file);
    } else {
        alert('No template file selected.');
    }
}

function renderTable(data = jsonData, parentElement = document.getElementById('jsonTable'), path = '') {
    parentElement.innerHTML = '';

    const table = document.createElement('table');
    parentElement.appendChild(table);

    const keys = Object.keys(data);
    if (keys.length > 0) {
        const headerRow = document.createElement('tr');

        const keyTh = document.createElement('th');
        keyTh.textContent = 'Key';
        headerRow.appendChild(keyTh);

        const valueTh = document.createElement('th');
        valueTh.textContent = 'Value';
        headerRow.appendChild(valueTh);

        const editTh = document.createElement('th');
        editTh.textContent = 'Edit';
        headerRow.appendChild(editTh);

        table.appendChild(headerRow);

        keys.forEach((key) => {
            const tr = document.createElement('tr');

            const keyTd = document.createElement('td');
            keyTd.textContent = key;
            tr.appendChild(keyTd);

            const valueTd = document.createElement('td');
            const value = data[key];

            if (Array.isArray(value)) {
                const expandButton = document.createElement('button');
                expandButton.textContent = 'Expand';
                const subContainer = document.createElement('div');
                subContainer.style.display = 'none';
                expandButton.addEventListener('click', () => {
                    if (expandButton.textContent === 'Expand') {
                        subContainer.style.display = 'block';
                        renderArray(value, subContainer, `${path}${key}.`);
                        expandButton.textContent = 'Collapse';
                    } else {
                        subContainer.style.display = 'none';
                        expandButton.textContent = 'Expand';
                    }
                });
                valueTd.appendChild(expandButton);
                valueTd.appendChild(subContainer);
            } else if (typeof value === 'object' && value !== null) {
                const expandButton = document.createElement('button');
                expandButton.textContent = 'Expand';
                const subContainer = document.createElement('div');
                subContainer.style.display = 'none';
                expandButton.addEventListener('click', () => {
                    if (expandButton.textContent === 'Expand') {
                        subContainer.style.display = 'block';
                        renderTable(value, subContainer, `${path}${key}.`);
                        expandButton.textContent = 'Collapse';
                    } else {
                        subContainer.style.display = 'none';
                        expandButton.textContent = 'Expand';
                    }
                });
                valueTd.appendChild(expandButton);
                valueTd.appendChild(subContainer);
            } else {
                if (typeof value === 'boolean') {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.checked = value;
                    checkbox.addEventListener('change', (event) => {
                        setDataByPath(path + key, event.target.checked);
                    });
                    valueTd.appendChild(checkbox);
                } else if (typeof value === 'number') {
                    const input = document.createElement('input');
                    input.type = 'number';
                    input.value = value;
                    input.addEventListener('change', (event) => {
                        setDataByPath(path + key, parseFloat(event.target.value));
                    });
                    valueTd.appendChild(input);
                } else {
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = value;
                    input.addEventListener('change', (event) => {
                        setDataByPath(path + key, event.target.value);
                    });
                    valueTd.appendChild(input);
                }
            }
            tr.appendChild(valueTd);

            const editTd = document.createElement('td');
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.onclick = () => {
                deleteDataByPath(path + key);
                renderTable();
            };
            editTd.appendChild(deleteButton);
            tr.appendChild(editTd);

            table.appendChild(tr);
        });
    } else {
        const noDataRow = document.createElement('tr');
        const noDataTd = document.createElement('td');
        noDataTd.colSpan = 3;
        noDataTd.textContent = 'No data available';
        noDataRow.appendChild(noDataTd);
        table.appendChild(noDataRow);
    }

    // Add a row for adding new key-value pairs
    const addRow = document.createElement('tr');
    const addKeyTd = document.createElement('td');
    const addKeyInput = document.createElement('input');
    addKeyInput.type = 'text';
    addKeyTd.appendChild(addKeyInput);
    addRow.appendChild(addKeyTd);

    const addValueTd = document.createElement('td');
    const addValueInput = document.createElement('input');
    addValueInput.type = 'text';
    addValueTd.appendChild(addValueInput);
    addRow.appendChild(addValueTd);

    const addEditTd = document.createElement('td');
    const addButton = document.createElement('button');
    addButton.textContent = 'Add';
    addButton.onclick = () => {
        const newKey = addKeyInput.value.trim();
        if (newKey) {
            data[newKey] = addValueInput.value;
            renderTable();
        } else {
            alert('Key cannot be empty');
        }
    };
    addEditTd.appendChild(addButton);
    addRow.appendChild(addEditTd);

    table.appendChild(addRow);
}

function renderArray(arr, parentElement, path) {
    parentElement.innerHTML = '';

    const list = document.createElement('ul');
    parentElement.appendChild(list);

    const expandedItems = []; // 用於存儲當前展開的項目索引

    arr.forEach((item, index) => {
        const listItem = document.createElement('li');
        listItem.dataset.id = index;

        const idLabel = document.createElement('span');
        idLabel.textContent = `ID: ${index} `;
        listItem.appendChild(idLabel);

        if (typeof item === 'object' && item !== null) {
            const expandButton = document.createElement('button');
            expandButton.textContent = 'Expand';
            const subContainer = document.createElement('div');
            subContainer.style.display = 'none';
            expandButton.addEventListener('click', () => {
                if (expandButton.textContent === 'Expand') {
                    subContainer.style.display = 'block';
                    renderTable(item, subContainer, `${path}${index}.`);
                    expandButton.textContent = 'Collapse';
                    expandedItems.push(index); // 記錄展開的項目索引
                } else {
                    subContainer.style.display = 'none';
                    expandButton.textContent = 'Expand';
                    expandedItems.splice(expandedItems.indexOf(index), 1); // 移除收起的項目索引
                }
            });
            listItem.appendChild(expandButton);
            listItem.appendChild(subContainer);
        } else {
            if (typeof item === 'boolean') {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.checked = item;
                checkbox.addEventListener('change', (event) => {
                    setDataByPath(`${path}${index}`, event.target.checked);
                });
                listItem.appendChild(checkbox);
            } else if (typeof item === 'number') {
                const input = document.createElement('input');
                input.type = 'number';
                input.value = item;
                input.addEventListener('change', (event) => {
                    setDataByPath(`${path}${index}`, parseFloat(event.target.value));
                });
                listItem.appendChild(input);
            } else {
                const input = document.createElement('input');
                input.type = 'text';
                input.value = item;
                input.addEventListener('change', (event) => {
                    setDataByPath(`${path}${index}`, event.target.value);
                });
                listItem.appendChild(input);
            }
        }

        list.appendChild(listItem);
    });

    new Sortable(list, {
        animation: 150,
        onEnd: function (evt) {
            const movedItem = arr.splice(evt.oldIndex, 1)[0];
            arr.splice(evt.newIndex, 0, movedItem);
    
            // 重新更新每個項目的 ID
            arr.forEach((item, index) => {
                if (item.hasOwnProperty('id')) {
                    item.id = index;
                }
            });
    
            renderTable(); // 重新渲染表格

            // 重新展開之前展開的項目
            expandedItems.forEach(index => {
                const expandButton = document.querySelector(`li[data-id="${index}"] button`);
                if (expandButton && expandButton.textContent === 'Expand') {
                    expandButton.click();
                }
            });
        }
    });

    const addButton = document.createElement('button');
    addButton.textContent = 'Add New Object';
    addButton.onclick = () => {
        // 顯示選擇 action 的選項
        const actionSelect = document.createElement('select');
        const actions = Object.keys(templates);
        actions.forEach(action => {
            const option = document.createElement('option');
            option.value = action;
            option.textContent = action;
            actionSelect.appendChild(option);
        });
        const confirmButton = document.createElement('button');
        confirmButton.textContent = 'Confirm';
        confirmButton.onclick = () => {
            const selectedAction = actionSelect.value;
            const newObject = JSON.parse(JSON.stringify(templates[selectedAction]));
            arr.push(newObject);
            renderTable();
        };
        parentElement.appendChild(actionSelect);
        parentElement.appendChild(confirmButton);
    };
    parentElement.appendChild(addButton);
}

function setDataByPath(path, value) {
    const keys = path.split('.');
    let obj = jsonData;
    keys.slice(0, -1).forEach(key => {
        obj = obj[key];
    });
    obj[keys[keys.length - 1]] = value;
}

function deleteDataByPath(path) {
    const keys = path.split('.');
    let obj = jsonData;
    keys.slice(0, -1).forEach(key => {
        obj = obj[key];
    });
    delete obj[keys[keys.length - 1]];
}

function downloadJSON() {
    const jsonStr = JSON.stringify(jsonData, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'data.json';
    a.click();
    URL.revokeObjectURL(url);
}
