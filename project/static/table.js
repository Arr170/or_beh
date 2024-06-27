
//posloucha a ceka na nacteni stranky, pak posle get request na data do tabulky a vygeneruje tabulku
document.addEventListener('DOMContentLoaded', function () {
    fetchJson_CreateTable()
})

//znovu posle request a vygeneruje tabulku pri zadani jmena
document.getElementById("filter-by-name").addEventListener('input', function () {
    fetchJson_CreateTable()
})

document.getElementById("track-select-id").addEventListener('change', function () {
    fetchJson_CreateTable()
})

//ted je to nastaveny tak, ze kazdy datum ma svoje vlastni poradi
document.getElementById("date-select-id").addEventListener('change', function () {
    fetchJson_CreateTable()
})

function formatTime(timeInSec) {
    var hours = Math.floor(timeInSec / 3600)
    var minutes = Math.floor((timeInSec - hours * 3600) / 60) % 60
    var seconds = timeInSec % 60
    return (hours < 10 ? ('0' + hours) : (hours)) + ':' + (minutes < 10 ? ('0' + minutes) : minutes) + ':' + (seconds < 10 ? ('0' + seconds) : seconds)
}


//fetchne data pro tabulku a vyvola funkci na tvoreni tabulky
function fetchJson_CreateTable() {
    return new Promise((resolve, reject) => {
        const nameFilter = document.getElementById("filter-by-name").value
        const trackFilter = document.getElementById("track-select-id").value
        const dateFilter = document.getElementById("date-select-id").value

        const url = new URL(document.URL + "data")
        if (nameFilter) {
            url.searchParams.append('name', nameFilter)
        }
        if (trackFilter !== "all") {
            url.searchParams.append('track', trackFilter)
        }
        if (dateFilter !== "all") {
            url.searchParams.append('date', dateFilter)
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                //console.log(data)
                createTable(data)
                resolve()
            })
            .catch(error => {
                console.error('Error fetching JSON:', error)
                reject(error)
            })

    })
}

//generuje tabulku
function createTable(data) {


    //najit tablku
    const table = document.getElementById("content-table")
    //vymazat vsechny radky
    table.innerHTML = ""
    const thead = document.createElement('thead')
    const theadRow = document.createElement('tr')
    const cols = Object.keys(data[0])

    //poradi se bude vytvare pouze kdyz zobrazuejeme jednu trat a nefiltrujeme dle jmena
    if (!document.getElementById("filter-by-name").value && document.getElementById("track-select-id").value !== "all") {
        const thPos = document.createElement('th')
        thPos.textContent = "#"
        theadRow.appendChild(thPos)
    }

    //kolonka na jmeno
    const thName = document.createElement('th')
    thName.textContent = "jméno"
    theadRow.appendChild(thName)

    //cas
    const thTime = document.createElement('th')
    thTime.textContent = "čas"
    theadRow.appendChild(thTime)

    //trat
    const thTrack = document.createElement('th')
    thTrack.textContent = "trať"
    theadRow.appendChild(thTrack)

    //datum
    const thDate = document.createElement('th')
    thDate.textContent = "datum"
    theadRow.appendChild(thDate)

    "{% if current_user.is_authenticated %}"
    const thBtns = document.createElement('th')
    theadRow.appendChild(thBtns)
    "{% endif %}"



    thead.appendChild(theadRow)
    table.appendChild(thead)

    const tbody = document.createElement('tbody')

    //data 
    let position = 1//bude zobrazovat umisteni ucastnika
    data.forEach(item => {

        const row = document.createElement('tr')
        row.id = item['id']

        if (!document.getElementById("filter-by-name").value && document.getElementById("track-select-id").value !== "all") {
            const tdPos = document.createElement('td')
            tdPos.textContent = position++ + '.'
            tdPos.id = "pos-" + item['id']
            row.appendChild(tdPos)
        }

        const tdName = document.createElement('td')
        //tdName.classList.add("text-center")
        tdName.textContent = item['name']
        tdName.onclick = () => { focusRow(item['id']) } //kliknutim na jmeno se zobrazi tabulka s jednou trati a nakliknuty zaznam se zvyrazni
        tdName.id = "name-" + item['id']
        row.appendChild(tdName)

        const tdTime = document.createElement('td')
        tdTime.textContent = formatTime(item['time'])
        tdTime.id = "time-" + item['id']
        row.appendChild(tdTime)

        const tdTrack = document.createElement('td')
        tdTrack.textContent = item['track']
        tdTrack.id = "track-" + item['id']
        row.appendChild(tdTrack)

        const tdDate = document.createElement('td')
        tdDate.textContent = item['date']
        tdDate.id = "date-" + item['id']
        row.appendChild(tdDate)

        //overit jestli admin je prihlasen, jestli ano, zobrazi ze tlacitka na upravu vysledku
        "{% if current_user.is_authenticated %}"
        const tdB = document.createElement('td')

        //mazaci tlacitko
        const deleteButton = document.createElement('button')
        deleteButton.id = "edit-button-" + item['id']
        deleteButton.textContent = "delete"
        deleteButton.classList.add("btn")
        deleteButton.classList.add("btn-danger")
        deleteButton.setAttribute("data-bs-toggle", "modal")
        deleteButton.setAttribute("data-bs-target", "#delete-modal")
        deleteButton.onclick = (() => {
            const modalName = document.getElementById("delete-name")
            modalName.textContent = document.getElementById("name-" + item['id']).textContent

            const modalTime = document.getElementById("delete-time")
            modalTime.textContent = "Čas: " + document.getElementById("time-" + item['id']).textContent

            const modalTrack = document.getElementById("delete-track")
            modalTrack.textContent = "Trať: " + document.getElementById("track-" + item['id']).textContent

            const modalId = document.getElementById("delete-id")
            modalId.textContent = item['id']
        })

        //upravovaci tlacitko
        const changeButton = document.createElement('button')
        changeButton.id = "change-button" + item['id']
        changeButton.textContent = "change"
        changeButton.classList.add("btn")
        changeButton.classList.add("btn-warning")
        changeButton.setAttribute("data-bs-toggle", "modal")
        changeButton.setAttribute("data-bs-target", "#change-modal")
        changeButton.onclick = (()=>{

            const modalNamechange = document.getElementById("change-name-input")
            modalNamechange.value = document.getElementById("name-" + item['id']).textContent

            const modalTime = document.getElementById("change-time")
            modalTime.textContent = "Čas: " + document.getElementById("time-" + item['id']).textContent

            const modalTrack = document.getElementById("change-track")
            modalTrack.textContent = "Trať: " + document.getElementById("track-" + item['id']).textContent

            const modalId = document.getElementById("change-id")
            modalId.textContent = item['id']
        })
        tdB.classList.add("text-center")
        tdB.appendChild(deleteButton)
        tdB.appendChild(changeButton)
        row.appendChild(tdB)

        "{% endif %}"
        tbody.appendChild(row)
    })
    table.appendChild(tbody)


}

function changeRslt(){
    const id = document.getElementById("change-id").textContent
    const close = document.getElementById("close-modal")
    const name = document.getElementById("change-name-input")
    const data = {
        name: name.value
    }
    close.click()
    const url = '{{url_for("main.rslt_change", id="")}}'
    fetch(url+id, 
        {
            method: "PUT", 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
    )
        .then(res=>console.log(res))
        .then(location.reload())
        .catch(error => {
                console.error('Error fetching JSON:', error)
            })
    
}

function deleteRslt() {
    const id = document.getElementById("delete-id").textContent
    const close = document.getElementById("close-modal")
    close.click()
    const url = '{{url_for("main.rslt_remove", id="")}}'
    fetch(url + id,
        { method: "DELETE" }
    )
        .then(res => console.log(res))
        .then(location.reload())
}

function focusRow(id) {
    const nameF = document.getElementById("filter-by-name")
    nameF.value = ''
    const track = document.getElementById("track-select-id")
    track.value = document.getElementById("track-" + id).textContent
    fetchJson_CreateTable().then(() => {
        const row = document.getElementById(id)
        row.scrollIntoView({ block: 'center', behavior: 'smooth' })
        row.style.borderColor = "yellow"
        document.getElementById("pos-" + id).style.color = "yellow"
        document.getElementById("name-" + id).style.color = "yellow"
        document.getElementById("date-" + id).style.color = "yellow"
        document.getElementById("time-" + id).style.color = "yellow"
        document.getElementById("track-" + id).style.color = "yellow"
    })
}

