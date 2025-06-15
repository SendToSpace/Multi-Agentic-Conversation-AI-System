// add exceptions for waitng server calling

//list of dictionaries
// [{"name": "item1", "quantity": 2, "unitPrice": 10.0, "total": 20.0}, {"name": "item2", "quantity": 3, "unitPrice": 5.0, "total": 15.0}]
let expense =[];

document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('h2');
    header.classList.add('fade-in');
});

function renderTable(){
   let grandTotal= 0; 
   const table= document.getElementById("expenseTable");
   table.innerHTML= "";
   
   expense.forEach((item,index) => {
    grandTotal=grandTotal+item.total; //calculate total
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
   document.getElementById("totalDisplay").style.color = "red";
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

async function process_img() {
    const fileInput = document.getElementById("imageUpload");
    const file = fileInput.files[0];
    document.getElementById("status").textContent = "正在处理...";
    fileInput.disabled = true;
    document.getElementById("imageUpload").disabled = true;
    
    if (fileInput.files.length === 0) {
        alert("请上传图片！");
        fileInput.disabled = false;
        document.getElementById("status").textContent="";
        return;
    }
    if (!file){
        alert("图片only！");
        return
    }
    const formData = new FormData();
    formData.append("image", file);

    try {
    const response = await fetch('http://127.0.0.1:5000/extract_text_from_document',{
        method: 'POST',
        body: formData,
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    json_array = await response.json();
    for (let i = 0; i < json_array.length; i++) {
        const item = json_array[i];
        expense.push({
            name: item.name,
            quantity: item.quantity,
            unitPrice: item.unitPrice,
            total: item.total
        });
    }
    document.getElementById("status").textContent = "Done！";
    renderTable();

    } catch (error) {
        console.error('Error:', error);
        document.getElementById("status").textContent = "云端down！";
    }   
}