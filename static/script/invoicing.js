let hoverBlue = "rgba(30,141,184,255)"
let table = document.getElementById("invoices");
let heading = document.createElement("tr");
heading.innerHTML = '<th>Invoice #</th><th>First Name</th><th>Last Name</th><th>Office Charges</th><th>Project Management</th><th>Travel Charges</th><th>Consultancy Charges</th>'
table.appendChild(heading);

let url = '/json';
let xhr = new XMLHttpRequest()
xhr.open("GET", url, true)
xhr.setRequestHeader("Accept", "invoice.json")

xhr.onload = function() {
    if (this.status === 200) {
        let data = JSON.parse(this.responseText);
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            let row = document.createElement("tr");
            
            let id = document.createElement("td");
            id.innerHTML = data[i].ID;
            row.appendChild(id);
            id.addEventListener('mouseover', function () {id.style.backgroundColor = hoverBlue})
            id.addEventListener('mouseout', function () {id.style.backgroundColor = 'white'})
            
            let firstName = document.createElement("td");
            firstName.innerHTML = data[i].first_name
            row.appendChild(firstName);
            firstName.addEventListener('mouseover', function () {firstName.style.backgroundColor = hoverBlue})
            firstName.addEventListener('mouseout', function () {firstName.style.backgroundColor = 'white'})
            firstName.addEventListener('click', function () {let newFirstName = prompt('First Name: ', data.First_Name); if(newFirstName != null){ firstName.innerHTML = newFirstName;data.First_Name = newFirstName;fetch('/add/UPDATE/'+data[i].ID+"/First_Name/"+newFirstName, {method: 'POST'})}})

            let lastName = document.createElement("td");
            lastName.innerHTML = data[i].Last_Name
            row.appendChild(lastName);
            lastName.addEventListener('mouseover', function () {lastName.style.backgroundColor = hoverBlue})
            lastName.addEventListener('mouseout', function () {lastName.style.backgroundColor = 'white'})
            lastName.addEventListener('click', function () {let newLastName = prompt('Last Name: ', data.Last_Name); if(newLastName != null){ lastName.innerHTML = newLastName;data.Last_Name = newLastName;fetch('/add/UPDATE/'+data[i].ID+"/Last_Name/"+newLastName, {method: 'POST'})}})
            
            let officeCharges = document.createElement("td");
            officeCharges.innerHTML = data[i].office_charges
            row.appendChild(officeCharges);
            officeCharges.addEventListener('mouseover', function () {officeCharges.style.backgroundColor = hoverBlue})
            officeCharges.addEventListener('mouseout', function () {officeCharges.style.backgroundColor = 'white'})
            officeCharges.addEventListener('click', function () {let newOfficeCharges = prompt('Office Charges: ', data[i].office_charges); if(newOfficeCharges != null){ officeCharges.innerHTML = newOfficeCharges;data.office_charges = newOfficeCharges;fetch('/add/UPDATE/'+data[i].ID+"/Office_Charges/"+newOfficeCharges, {method: 'POST'})}})

            let projectManagement = document.createElement("td");
            projectManagement.innerHTML = data[i].project_management
            row.appendChild(projectManagement);
            projectManagement.addEventListener('mouseover', function () {projectManagement.style.backgroundColor = hoverBlue})
            projectManagement.addEventListener('mouseout', function () {projectManagement.style.backgroundColor = 'white'})
            projectManagement.addEventListener('click', function () {let newProjectManagement = prompt('Project Management: ', data.Project_Management); if(newProjectManagement != null){ projectManagement.innerHTML = newProjectManagement;data.project_management = newProjectManagement;fetch('/add/UPDATE/'+data[i].ID+"/Project_Management/"+newProjectManagement, {method: 'POST'})}})

            let travelCharges = document.createElement("td");
            travelCharges.innerHTML = data[i].travel_charges
            row.appendChild(travelCharges);
            travelCharges.addEventListener('mouseover', function () {travelCharges.style.backgroundColor = hoverBlue})
            travelCharges.addEventListener('mouseout', function () {travelCharges.style.backgroundColor = 'white'})
            travelCharges.addEventListener('click', function () {let newTravelCharges = prompt('Travel Charges: ', data.Travel_Charges); if(newTravelCharges != null){ travelCharges.innerHTML = newTravelCharges;data.travel_charges = newTravelCharges;fetch('/add/UPDATE/'+data[i].ID+"/Travel_Charges/"+newTravelCharges, {method: 'POST'})}})

            let consultancyCharges = document.createElement("td");
            consultancyCharges.innerHTML = data[i].consultancy_charges
            row.appendChild(consultancyCharges);
            consultancyCharges.addEventListener('mouseover', function () {consultancyCharges.style.backgroundColor = hoverBlue})
            consultancyCharges.addEventListener('mouseout', function () {consultancyCharges.style.backgroundColor = 'white'})
            consultancyCharges.addEventListener('click', function () {let newConsultancyCharges = prompt('Consultancy Charges: ', data.Consultancy_Charges); if(newConsultancyCharges != null){ consultancyCharges.innerHTML = newConsultancyCharges;data.consultancy_charges = newConsultancyCharges;fetch('/add/UPDATE/'+data[i].ID+"/Consultancy_Charges/"+newConsultancyCharges, {method: 'POST'})}})

            let deleteButton = document.createElement("button");
            deleteButton.innerHTML = "Delete"
            row.appendChild(deleteButton);
            deleteButton.addEventListener("click", function(){fetch("/add/DELETE/"+data[i].ID+"/row/Null", {method: 'POST'});row.remove();})

            table.appendChild(row);
        }
    }
}
xhr.send()