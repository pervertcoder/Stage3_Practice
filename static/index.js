"use strict";

// 存到暫存
let check = localStorage.getItem("photoArr");
if (check) {
  console.log("有資料了");
} else {
  let uploadPhotos = [];
  const uploadPhotosStr = JSON.stringify(uploadPhotos);
  localStorage.setItem("photoArr", uploadPhotosStr);
}

const renderDiv = function (m = null, photoPath = null) {
  const messageFather = document.querySelector(".messageBox");
  const messageDiv = document.createElement("div");
  messageDiv.className = "messageBox__son";
  messageFather.appendChild(messageDiv);
  const messageP = document.createElement("p");
  messageP.className = "messageP";
  messageDiv.appendChild(messageP);
  const imgHolder = document.createElement("img");
  imgHolder.className = "imgHolder";
  messageDiv.appendChild(imgHolder);
  messageP.textContent = m;
  imgHolder.src = photoPath;
  imgHolder.alt = "photo";
};

// 拿圖片出來
const photoUse = localStorage.getItem("photoArr");
const photoUseArr = JSON.parse(photoUse);
const render = async function () {
  const url = "/api/render";
  const req = await fetch(url);

  const response = await req.json();
  console.log(response);

  const messageContent = response.data.msg;
  for (let i = 0; i < messageContent.length; i++) {
    renderDiv(response.data.msg[i], photoUseArr[i]);
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
    if (file) {
      const formData = new FormData();
      formData.append("file", file);
      console.log(formData);
      const url2 = "/api/upload";
      const request = await fetch(url2, {
        method: "POST",
        body: formData,
      });

      const response2 = await request.json();
      console.log(response2);
      const photoPlace = response2.data.path;

      let photoStorage = localStorage.getItem("photoArr");
      let photoStorageUse = JSON.parse(photoStorage);
      photoStorageUse.push("/" + photoPlace);
      let photoInAgain = JSON.stringify(photoStorageUse);
      localStorage.setItem("photoArr", photoInAgain);

      window.location.reload();
    } else {
      alert("請選擇圖片");
      return;
    }
  }
});

const deleteBtn = document.getElementById("delete");

deleteBtn.addEventListener("click", async () => {
  const url = "/api/delete";
  const request = await fetch(url, {
    method: "delete",
  });

  const response = await request.json();
  localStorage.clear();
  console.log(response);
  console.log("清空成功");
  window.location.reload();
});
