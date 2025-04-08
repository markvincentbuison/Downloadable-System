
// Object containing the features data for each system
const featuresData = {
  AI: [
    {
      feature: "AI-based Data Analytics",
      image: "/static/uploads/ai.png", // Corrected AMS image path
      downloadLink: "/static/downloads/AI-based-Data-Analytics.msi", // Path to the downloadable file
      
    },
    "AI-based Data Analytics",
    "Automation Framework",
    "Machine Learning Integrations",
    "AI-driven Decision Support",
    "Predictive Maintenance Modules",
  ],
  AMS: [
    {
      feature: "Alumni Management System (AMS)",
      image: "/static/uploads/alumni.png",
      width: "20px",
      height: "50px",
      downloadLink: "/static/downloads/Alumni-Management-System-(AMS).msi", // Path to the downloadable file
    },
    "Event & Engagement Tracking",
    "Alumni Networking Features",
    "Donations & Fundraising Tools",
    "Alumni News Feed",
  ],
  CRM: [
    {
      feature: "Customer Relationship Management (CRM) System",
      image: "/static/uploads/crm.png", // Corrected AMS image path
      downloadLink: "/static/downloads/Customer-Relationship-Management-(CRM)-System.exe", // Path to the downloadable file
    },
    "Customer Relationship Management",
    "Sales Pipeline Management",
    "Lead Scoring",
    "Automated Customer Support",
    "Customer Analytics",
  ],
  Cybersecurity: [
    {
      feature: "Cybersecurity System",
      image: "/static/uploads/cyber.png", // Corrected Cybersecurity image path
      downloadLink: "/static/downloads/Cybersecurity-System.exe", // Path to the downloadable file
    },
    "Intrusion Detection Systems (IDS)",
    "Firewall Management",
    "Threat Intelligence Integration",
    "Data Encryption",
    "Multi-factor Authentication",
  ],
  DevOps: [
    {
      feature: "DevOps & Deployment Modules",
      image: "/static/uploads/devops.png", // Corrected DevOps & Deployment Modules image path
      downloadLink: "/static/downloads/DevOps-&-Deployment-Modules.msi", // Path to the downloadable file
    },
    "Continuous Integration/Continuous Deployment (CI/CD)",
    "Version Control Integration",
    "Automated Testing",
    "Monitoring & Logging",
    "Infrastructure as Code",
  ],
  E_commerce: [
    {
      feature: "E-commerce Platforms",
      image: "/static/uploads/ecom.png", // Corrected E-commerce Platforms image path
      downloadLink: "/static/downloads/E-commerce-Platforms.msi", // Path to the downloadable file
    },
    "Product Catalog Management",
    "Shopping Cart & Checkout",
    "Order Management",
    "Payment Gateway Integration",
    "Customer Reviews & Ratings",
    "Discount & Coupon Management",
    "Inventory Management",
    "Shipping & Logistics Integration",
    "Multi-channel Sales Integration",
  ],
  ERP: [
    {
      feature: "Enterprise Resource Planning (ERP)",
      image: "/static/uploads/erp.png", // Corrected Enterprise Resource Planning (ERP) image path
      downloadLink: "/static/downloads/Enterprise-Resource-Planning-(ERP).msi", // Path to the downloadable file
    },
    "Enterprise Resource Planning",
    "Inventory Management",
    "Financial Reporting",
    "Human Resources Management",
    "Supply Chain Management",
  ],
  HRMS: [
    {
      feature: "HR Management System (HRMS)",
      image: "/static/uploads/hrms.png", // Corrected HR Management System (HRMS) image path
      downloadLink: "/static/downloads/HR-Management-System-(HRMS).msi", // Path to the downloadable file
    },
    "Employee Records Management",
    "Payroll Management",
    "Attendance Tracking",
    "Performance Management",
    "Employee Benefits Management",
  ],
  ITSM: [
    {
      feature: "Advanced IT Service Management (ITSM)",
      image: "/static/uploads/itsm.png", // Corrected Advanced IT Service Management (ITSM) image path
      downloadLink: "/static/downloads/Advanced-IT-Service-Management-(ITSM).msi", // Path to the downloadable file
    },
    "Incident Management",
    "Service Catalog",
    "Change Management",
    "Problem Management",
    "Knowledge Base",
  ],
  LMS: [
    {
      feature: "Learning Management System (LMS)",
      image: "/static/uploads/lms.png", // Corrected Learning Management System (LMS) image path
      downloadLink: "/static/downloads/Learning-Management-System-(LMS).msi", // Path to the downloadable file
    },
    "Course Management",
    "Student Enrollment",
    "Assessments & Certifications",
    "Learning Pathways",
    "Online Discussion Forums",
  ],
  PMT: [
    {
      feature: "Project Management Tools",
      image: "/static/uploads/pmt.png", // Corrected Project Management Tools image path
      downloadLink: "/static/downloads/Project-Management-Tools.msi", // Path to the downloadable file
    },
    "Task Assignment & Tracking",
    "Project Timelines",
    "Team Collaboration",
    "Resource Allocation",
    "Project Budgeting",
  ],
  POS: [
    {
      feature: "Online POS System",
      image: "/static/uploads/pos.png", // Corrected Online POS System image path
      downloadLink: "/static/downloads/Online-POS-System.msi", // Path to the downloadable file
    },
    "Point of Sale",
    "Inventory Management",
    "Sales Reporting",
    "Barcode Scanning",
    "Payment Integration",
  ],
  SystemUtilities: [
    {
      feature: "System Utilities & Services",
      image: "/static/uploads/utility.png", // Corrected System Utilities & Services image path
      downloadLink: "/static/downloads/System-Utilities-&-Services.msi", // Path to the downloadable file
    },
    "Disk Cleanup & Optimization",
    "Data Backup & Recovery",
    "System Monitoring",
    "Security Scanning",
    "Task Automation",
  ],
  UI: [
    {
      feature: "Frontend & UI Modules",
      image: "/static/uploads/frontend.png", // Corrected Frontend & UI Modules image path
      downloadLink: "/static/downloads/Frontend-&-UI-Modules.msi", // Path to the downloadable file
    },
    "UI Design Tools",
    "Frontend Frameworks (e.g., React, Vue.js)",
    "Responsive Design",
    "Animation & Transitions",
    "User Experience Research",
  ],
};

// Event listener for when the user selects a system
document.getElementById("systemSelect").addEventListener("change", function () {
  const selectedValue = this.value; // Get selected system
  const featureContent = document.getElementById("featureContent");

  // Clear the feature content before adding new features
  featureContent.innerHTML = "";

  // Check if the selected system exists in the features data
  if (featuresData[selectedValue]) {
    const ul = document.createElement("ul"); // Create an unordered list

    // Iterate over the features of the selected system
    featuresData[selectedValue].forEach(function (item) {
      if (typeof item === "object" && item.feature && item.image) {
        // If the item is an object with both feature and image properties
        const li = document.createElement("li");

        // Create and append the image
        const img = document.createElement("img");
        img.src = item.image;
        img.alt = item.feature;
        img.style.width = "100%"; // Optional: Style the image
        li.appendChild(img);

        // Create and append the feature text
        const featureText = document.createElement("p");
        featureText.textContent = item.feature;
        li.appendChild(featureText);

        // Check if there's a download link and add it
        if (item.downloadLink) {
          const downloadBtn = document.createElement("button");
          downloadBtn.textContent = "⬇️ Download";
          downloadBtn.className = "btn btn-sm btn-success mt-2";
          downloadBtn.setAttribute("type", "button");

          // Add event listener for the download button
          downloadBtn.addEventListener("click", function () {
            // Set the download link dynamically
            const confirmBtn = document.getElementById("confirmDownloadBtn");

            // Confirm download when the user clicks "Yes, Download"
            confirmBtn.onclick = function () {
              // Close the modal manually
              const modalEl = document.getElementById("downloadModal");
              const modalInstance = bootstrap.Modal.getInstance(modalEl);
              modalInstance.hide();

              // Start the download
              const tempLink = document.createElement("a");
              tempLink.href = item.downloadLink; // Use the download link from the item
              tempLink.setAttribute("download", "");
              tempLink.click();
            };

            // Show the Bootstrap modal
            const modal = new bootstrap.Modal(document.getElementById("downloadModal"));
            modal.show(); // Show confirmation modal
          });

          // Append the download button to the list item
          li.appendChild(downloadBtn);
        }

        // Append the list item to the unordered list
        ul.appendChild(li);
      } else {
        // If the item is a simple feature string (not an object)
        const li = document.createElement("li");
        li.textContent = item;
        ul.appendChild(li);
      }
    });

    // Append the unordered list to the feature content section
    featureContent.appendChild(ul);
  }
  
});
