async function fetchHoistHours() {
  try {
      const hoists = ["17", "33"]; // Add more hoists as needed
      for (const hoist of hoists) {
          const response = await fetch(`http://10.92.221.32:8000/get_hoist_hours_${hoist}`);
          if (!response.ok) throw new Error(`Failed to fetch hoist data for ${hoist}`);
          const data = await response.json();

          // Update table data
          document.getElementById(`Hoist${hoist}`).innerText = (data.hoist_hours / 60).toFixed(2);
          document.getElementById(`Trolly${hoist}`).innerText = (data.trolley_hours / 60).toFixed(2);
          document.getElementById(`Gantry${hoist}`).innerText = (data.gantry_hours / 60).toFixed(2);
          document.getElementById(`Control${hoist}`).innerText = (data.control_on_hours / 1).toFixed(0);

          // Battery level (specific to hoist 33)
          if (hoist === "33") {
              document.getElementById(`Battery${hoist}`).innerText = 
                  ((data.soc1 + data.soc2 + data.soc3) / 3).toFixed(0) + "%";
          }

          // Update indicator dynamically
          updateIndicatorStatus(hoist, data.control_on_state); // Use actual API field for "active"
      }
  } catch (error) {
      console.error("Error fetching hoist hours:", error);
  }
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
