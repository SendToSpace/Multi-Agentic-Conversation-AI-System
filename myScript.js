
let expense =[];

function renderTable(){
   let grandTotal= 0; 
   const table= document.getElementById("expenseTable");
   table.innerHTML= "";

   expense.forEach((item,index) => {
    grandTotal += item.total; //calculate total
    const row = document.createElement("tr");
    row.innerHTML =`
        <td>
            <input type="text" value="${item.name}" 
            onchange="updateItem(${index}, 'name', this.value)">
        </td>
         <td>
            <input type="number" value="${item.quantity}" 
            onchange="updateItem(${index}, 'quantity', this.value)">
        </td>
         <td>
            <input type="number" value="${item.unitPrice.toFixed(2)}" 
            onchange="updateItem(${index}, 'unitPrice', this.value)">
        </td>
         <td>
            <input type="number" value="${item.total}" 
            onchange="updateItem(${index}, 'total', this.value)">
        </td>
        <td>
        <button onclick="removeItem(${index})">🗑️ 删除</button>
        </td>
            `;

        table.appendChild(row)
   });
   document.getElementById("totalDisplay").textContent = `总计: ¥${grandTotal.toFixed(2)}`;
}

function updateItem(index, key, value) {
    if (key === "quantity" || key === "unitPrice" || key ==='total') {
        value = parseFloat(value);
        if (isNaN(value) || value < 0) {
            alert(`重新输入${key}`);
            return;
        }
    }
    expense[index][key] = value;
    renderTable();
}

function removeItem(index) {
  expense.splice(index, 1);
    renderTable();
}

function addRow() {
    expense.push({
        name: "",
        quantity: 0,
        unitPrice:0.0,
        total: 0.0
    });
    renderTable();
}
renderTable();