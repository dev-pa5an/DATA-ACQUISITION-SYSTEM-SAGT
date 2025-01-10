async function fetchHoistHours() {
    const cranes = ["09", "17", "23", "33", "34"]; // List of hoists
    
    cranes.forEach(async (crane) => {
        try {
            const response = await fetch(`http://10.92.221.32:8000/get_hoist_hours_${crane}`);
            if (!response.ok) {
                console.error(`Failed to fetch hoist data for ${crane}: ${response.status} ${response.statusText}`);
                handleMissingCraneData(crane); // Handle the failure case immediately
                return;
            }
            
            const data = await response.json();
            updateCraneData(crane, data); // Update the page immediately with the returned data
        } catch (error) {
            console.error(`Error fetching data for crane ${crane}:`, error);
            handleMissingCraneData(crane); // Handle the error case immediately
        }
    });
}

function updateCraneData(crane, data) {
    // Update table data
    document.getElementById(`Hoist${crane}`).innerText = (data.hoist_hours ? (data.hoist_hours / 60).toFixed(2) : "N/A");
    document.getElementById(`Trolly${crane}`).innerText = (data.trolley_hours ? (data.trolley_hours / 60).toFixed(2) : "N/A");
    document.getElementById(`Gantry${crane}`).innerText = (data.gantry_hours ? (data.gantry_hours / 60).toFixed(2) : "N/A");
    document.getElementById(`Control${crane}`).innerText = (data.control_on_hours ? (data.control_on_hours / 1).toFixed(0) : "N/A");

    // Update battery level (if applicable)
    if (["33", "09", "23", "17"].includes(crane) && data.soc1 !== undefined && data.soc2 !== undefined && data.soc3 !== undefined) {
        document.getElementById(`Battery${crane}`).innerText =
            ((data.soc1 + data.soc2 + data.soc3) / 3).toFixed(0) + "%";
    }

    // Update indicator dynamically
    updateIndicatorStatus(crane, data.control_on_state);
}

function handleMissingCraneData(crane) {
    console.warn(`No data available for crane ${crane}. Setting default values.`);
    document.getElementById(`Hoist${crane}`).innerText = "N/A";
    document.getElementById(`Trolly${crane}`).innerText = "N/A";
    document.getElementById(`Gantry${crane}`).innerText = "N/A";
    document.getElementById(`Control${crane}`).innerText = "N/A";
    document.getElementById(`Battery${crane}`).innerText = "N/A";
    updateIndicatorStatus(crane, false); // Default to "inactive"
}

const updateIndicatorStatus = (suffix, isActive) => {
    const indicatorElement = document.getElementById(`Indicator${suffix}`);
    if (indicatorElement) {
        const img = document.createElement('img');
        img.src = isActive ? '/static/green.png' : '/static/red.png';
        img.style.width = '30px';
        img.style.height = '30px';
        indicatorElement.innerHTML = ''; // Clear previous content
        indicatorElement.appendChild(img);
    }
};

// Initial fetch and set refresh interval
fetchHoistHours();
setInterval(fetchHoistHours, 60000);
