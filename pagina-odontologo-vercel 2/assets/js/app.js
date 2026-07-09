(function () {
  const data = window.siteData;

  if (!data) {
    return;
  }

  const getValue = (path) =>
    path.split(".").reduce((value, key) => (value ? value[key] : ""), data) || "";

  const setTextContent = () => {
    document.querySelectorAll("[data-text]").forEach((element) => {
      const value = getValue(element.dataset.text);
      if (value) {
        element.textContent = value;
      }
    });
  };

  const buildWhatsappUrl = (message) => {
    const number = data.contact.whatsapp.replace(/\D/g, "");
    return `https://wa.me/${number}?text=${encodeURIComponent(message)}`;
  };

  const setLinks = () => {
    const defaultMessage = `Hola, quisiera hacer una consulta en ${data.doctor.name}.`;

    document.querySelectorAll("[data-whatsapp-link]").forEach((link) => {
      link.href = buildWhatsappUrl(defaultMessage);
      link.target = "_blank";
    });

    document.querySelectorAll("[data-phone-link]").forEach((link) => {
      link.href = `tel:${data.contact.phone.replace(/\s/g, "")}`;
    });

    document.querySelectorAll("[data-maps-link]").forEach((link) => {
      link.href = data.contact.mapsUrl;
    });
  };

  const setImagesAndMap = () => {
    const logoImage = document.querySelector("[data-logo-image]");
    const heroImage = document.querySelector("[data-hero-image]");
    const profileImage = document.querySelector("[data-profile-image]");
    const mapFrame = document.querySelector("[data-map-frame]");

    if (logoImage) {
      logoImage.src = data.doctor.logoImage;
      logoImage.alt = "";
    }

    if (heroImage) {
      heroImage.onerror = () => {
        heroImage.src = "assets/img/og-preview.svg";
      };
      heroImage.src = data.hero.image;
      heroImage.alt = data.hero.imageAlt;
    }

    if (profileImage) {
      profileImage.src = data.doctor.profileImage;
      profileImage.alt = data.doctor.profileImageAlt || `Foto profesional de ${data.doctor.name}`;
    }

    if (mapFrame) {
      mapFrame.src = data.contact.mapsEmbedUrl;
    }
  };

  const renderHighlights = () => {
    const list = document.querySelector('[data-list="doctor.highlights"]');
    if (!list) {
      return;
    }

    list.innerHTML = data.doctor.highlights
      .map((item) => `<li>${item}</li>`)
      .join("");
  };

  const renderServices = () => {
    const container = document.querySelector("[data-services]");
    if (!container) {
      return;
    }

    container.innerHTML = data.services
      .map(
        (service, index) => `
          <article class="service-card">
            <span class="card-icon" aria-hidden="true">${String(index + 1).padStart(2, "0")}</span>
            <h3>${service.title}</h3>
            <p>${service.description}</p>
          </article>
        `
      )
      .join("");
  };

  const renderClinicGallery = () => {
    const container = document.querySelector("[data-clinic-gallery]");
    if (!container || !data.clinic?.photos?.length) {
      return;
    }

    container.innerHTML = data.clinic.photos
      .map(
        (photo) => `
          <figure class="clinic-photo">
            <img src="${photo.src}" alt="${photo.alt}" loading="lazy" />
          </figure>
        `
      )
      .join("");
  };

  const renderReasonOptions = () => {
    const select = document.querySelector("[data-reason-select]");
    if (!select) {
      return;
    }

    data.services.forEach((service) => {
      const option = document.createElement("option");
      option.value = service.title;
      option.textContent = service.title;
      select.appendChild(option);
    });
  };

  const renderContact = () => {
    const container = document.querySelector("[data-contact-list]");
    if (!container) {
      return;
    }

    const renderValue = (value) => {
      if (Array.isArray(value)) {
        return `
          <ul class="schedule-list">
            ${value
              .map(
                (item) => `
                  <li>
                    <span>${item.day}</span>
                    <strong>${item.time}</strong>
                  </li>
                `
              )
              .join("")}
          </ul>
        `;
      }

      return `<strong>${value}</strong>`;
    };

    const items = [
      ["Telefono", data.contact.phoneDisplay],
      ["WhatsApp", data.contact.whatsappDisplay],
      ["Direccion", data.contact.address],
      ["Horarios", data.contact.hours],
      ["Email", data.contact.email],
      ["Medios de pago", data.contact.paymentMethods],
    ].filter(([, value]) => (Array.isArray(value) ? value.length > 0 : Boolean(value)));

    container.innerHTML = items
      .map(
        ([label, value]) => `
          <div class="contact-item">
            <span>${label}</span>
            ${renderValue(value)}
          </div>
        `
      )
      .join("");
  };

  const renderFaqs = () => {
    const container = document.querySelector("[data-faq]");
    if (!container) {
      return;
    }

    container.innerHTML = data.faqs
      .map(
        (item) => `
          <details class="faq-item">
            <summary>${item.question}</summary>
            <p>${item.answer}</p>
          </details>
        `
      )
      .join("");
  };

  const renderSocial = () => {
    const container = document.querySelector("[data-social-links]");
    if (!container) {
      return;
    }

    const socialLinks = data.social.filter((item) => item.url);
    container.innerHTML = socialLinks.length
      ? socialLinks
          .map(
            (item) =>
              `<a href="${item.url}" target="_blank" rel="noopener">${item.name}</a>`
          )
          .join("")
      : "<p>Sin redes cargadas</p>";
  };

  const setupForm = () => {
    const form = document.querySelector("[data-appointment-form]");
    const status = document.querySelector("[data-form-status]");
    const dateInput = document.querySelector("#preferredDate");

    if (dateInput) {
      dateInput.min = new Date().toISOString().split("T")[0];
      setupDateShortcuts(dateInput);
    }

    if (!form) {
      return;
    }

    form.addEventListener("submit", (event) => {
      event.preventDefault();

      const formData = new FormData(form);
      const appointment = Object.fromEntries(formData.entries());

      if (!appointment.patientName || !appointment.phone || !appointment.reason) {
        if (status) {
          status.textContent = "Revisa los campos obligatorios antes de enviar.";
        }
        return;
      }

      sendAppointmentRequest(appointment);

      if (status) {
        status.textContent = "Se abrio WhatsApp con la solicitud lista para enviar.";
      }
    });
  };

  const setupDateShortcuts = (dateInput) => {
    const container = document.querySelector("[data-date-shortcuts]");
    if (!container) {
      return;
    }

    const dayMap = {
      Domingo: 0,
      Lunes: 1,
      Martes: 2,
      Miercoles: 3,
      Miércoles: 3,
      Jueves: 4,
      Viernes: 5,
      Sabado: 6,
      Sábado: 6,
    };
    const openDays = new Set(data.contact.hours.map((item) => dayMap[item.day]));
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const toInputValue = (date) => {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    };

    const formatButtonLabel = (date) => {
      const diffDays = Math.round((date - today) / 86400000);
      if (diffDays === 0) {
        return "Hoy";
      }
      if (diffDays === 1) {
        return "Mañana";
      }

      return new Intl.DateTimeFormat("es-AR", {
        weekday: "short",
        day: "numeric",
        month: "short",
      }).format(date);
    };

    const dates = [];
    const cursor = new Date(today);
    while (dates.length < 5) {
      if (openDays.has(cursor.getDay())) {
        dates.push(new Date(cursor));
      }
      cursor.setDate(cursor.getDate() + 1);
    }

    container.innerHTML = dates
      .map(
        (date) => `
          <button type="button" class="date-chip" data-date-value="${toInputValue(date)}">
            ${formatButtonLabel(date)}
          </button>
        `
      )
      .join("");

    const updateSelected = () => {
      container.querySelectorAll("[data-date-value]").forEach((button) => {
        button.classList.toggle("is-selected", button.dataset.dateValue === dateInput.value);
      });
    };

    container.addEventListener("click", (event) => {
      const button = event.target.closest("[data-date-value]");
      if (!button) {
        return;
      }

      dateInput.value = button.dataset.dateValue;
      dateInput.dispatchEvent(new Event("change", { bubbles: true }));
      updateSelected();
    });

    dateInput.addEventListener("change", updateSelected);
    updateSelected();
  };

  const sendAppointmentRequest = (appointment) => {
    const messageLines = [
      data.appointments.defaultWhatsappMessage,
      "",
      `Nombre: ${appointment.patientName}`,
      `Telefono: ${appointment.phone}`,
      `Email: ${appointment.email || "No informado"}`,
      `Motivo: ${appointment.reason}`,
      `Fecha preferida: ${appointment.preferredDate}`,
      `Horario preferido: ${appointment.preferredTime}`,
      `Mensaje: ${appointment.message || "Sin mensaje adicional"}`,
    ];

    window.open(buildWhatsappUrl(messageLines.join("\n")), "_blank", "noopener");

    // Futuro: reemplazar esta llamada por una API para guardar el turno.
    saveAppointmentDraft(appointment);
  };

  const saveAppointmentDraft = (appointment) => {
    const serialized = JSON.stringify({
      ...appointment,
      status: "pendiente",
      createdAt: new Date().toISOString(),
    });

    sessionStorage.setItem("lastAppointmentDraft", serialized);
  };

  const setupNavigation = () => {
    const button = document.querySelector("[data-nav-toggle]");
    const nav = document.querySelector("[data-nav]");
    const header = document.querySelector("[data-header]");

    if (!button || !nav) {
      return;
    }

    button.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(isOpen));
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        nav.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
      });
    });

    const updateHeader = () => {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
    };

    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });
  };

  const setupSeo = () => {
    const title = `${data.doctor.name} | Consultorio odontologico`;
    const description = `${data.hero.title}. Turnos, servicios, direccion y contacto por WhatsApp.`;

    document.title = title;
    document.querySelector('meta[name="description"]').setAttribute("content", description);
    document.querySelector('meta[property="og:title"]').setAttribute("content", title);
    document
      .querySelector('meta[property="og:description"]')
      .setAttribute("content", description);

    const schema = {
      "@context": "https://schema.org",
      "@type": "Dentist",
      name: data.doctor.name,
      description,
      telephone: data.contact.phone,
      email: data.contact.email,
      address: data.contact.address,
      openingHours: data.contact.hours
        .map((item) => `${item.day}: ${item.time}`)
        .join("; "),
      url: window.location.href,
    };

    const script = document.createElement("script");
    script.type = "application/ld+json";
    script.textContent = JSON.stringify(schema);
    document.head.appendChild(script);
  };

  document.addEventListener("DOMContentLoaded", () => {
    setTextContent();
    setLinks();
    setImagesAndMap();
    renderHighlights();
    renderClinicGallery();
    renderServices();
    renderReasonOptions();
    renderContact();
    renderFaqs();
    renderSocial();
    setupForm();
    setupNavigation();
    setupSeo();
  });
})();
