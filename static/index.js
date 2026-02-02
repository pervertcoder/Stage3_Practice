"use strict";

const renderDiv = function (m) {
  const messageFather = document.querySelector(".messageBox");
  const messageDiv = document.createElement("div");
  messageDiv.className = "messageBox__son";
  messageFather.appendChild(messageDiv);
  const messageP = document.createElement("p");
  messageP.className = "messageP";
  messageDiv.appendChild(messageP);
  messageP.textContent = m;
};

const render = async function () {
  const url = "/api/render";
  const req = await fetch(url);

  const response = await req.json();
  console.log(response);

  const messageContent = response.data.msg;
  for (let i = 0; i < messageContent.length; i++) {
    renderDiv(response.data.msg[i]);
  }
};

render();
const chooseFile = document.getElementById("chooseFile");
const submitFile = document.getElementById("submitFile");

submitFile.addEventListener("click", async () => {
  const message = document.getElementById("message").value.trim();
  const payload = {
    data: {
      content: message,
    },
  };
  if (!payload.data.content) {
    alert("請輸入訊息");
    return;
  } else {
    const url = "/api/insert";
    const req = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/JSON",
      },
      body: JSON.stringify(payload),
    });

    const response = await req.json();
    console.log(response);

    // 上傳圖片
    const photoFile = document.getElementById("photoUpload");
    const file = photoFile.files[0];
    const formData = new FormData();
    formData.append("file", file);
    console.log(formData);
    const url2 = "/api/upload";
    const request = await fetch(url2, {
      method: "POST",
      body: formData,
    });

    const response2 = await request.json();
    window.location.reload();
  }
});
