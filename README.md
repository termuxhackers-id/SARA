
        const monthName = document.getElementById('month-name');<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ปฏิทินวันพระ - โดยเณรปลื้ม</title>
    <link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #d4a017;
            --bg: #f0f2f5;
            --white: #ffffff;
            --text: #333;
            --holy-day-bg: #fff9db;
        }

        body { 
            font-family: 'Chakra Petch', sans-serif; 
            background-color: var(--bg); 
            margin: 0; padding: 0; 
            display: flex; flex-direction: column; align-items: center;
        }

        header {
            background: linear-gradient(135deg, #d4a017, #b8860b);
            color: white; width: 100%; text-align: center;
            padding: 30px 0; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .calendar-container {
            background: var(--white);
            width: 90%; max-width: 400px;
            margin: -20px auto 20px auto; border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden; padding-bottom: 20px;
            z-index: 10;
        }

        .month-header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 20px; font-weight: bold; font-size: 20px; color: var(--primary);
        }

        .weekdays {
            display: grid; grid-template-columns: repeat(7, 1fr);
            text-align: center; font-weight: bold; color: #999;
            padding-bottom: 10px;
        }

        .days {
            display: grid; grid-template-columns: repeat(7, 1fr);
            text-align: center;
        }

        .day {
            padding: 15px 0; position: relative; cursor: pointer;
            border-radius: 50%; transition: 0.2s; font-size: 16px;
            width: 40px; height: 40px; margin: 5px auto;
            display: flex; align-items: center; justify-content: center;
        }

        .day:hover { background: #f0f0f0; }

        .holy-day {
            background-color: var(--holy-day-bg);
            color: var(--primary); font-weight: bold;
            border: 1px solid var(--primary);
        }

        .holy-day::after {
            content: '🪷';
            position: absolute; bottom: -5px; font-size: 10px;
        }

        .today { background: var(--primary) !important; color: white !important; }

        /* Modal Popup */
        .modal {
            display: none; position: fixed; top: 0; left: 0;
            width: 100%; height: 100%; background: rgba(0,0,0,0.5);
            justify-content: center; align-items: center; z-index: 1000;
        }

        .modal-content {
            background: white; padding: 30px; border-radius: 20px;
            width: 80%; max-width: 300px; text-align: center;
        }

        .btn-close {
            margin-top: 20px; background: var(--primary);
            color: white; border: none; padding: 10px 20px;
            border-radius: 10px; cursor: pointer; font-family: 'Chakra Petch';
        }

        footer {
            margin: 20px 0; color: #777; font-size: 14px; text-align: center;
        }
    </style>
</head>
<body>

<header>
    <h1>ปฏิทินวันพระ วัดสมุหเขตตาราม วัดหัววัง ๒๕๖๙</h1>
    <p>สืบทอดพระพุทธศาสนา วันพระนี้ทำบุญกันนะ</p>
</header>

<div class="calendar-container">
    <div class="month-header">
        <button style="border:none; background:none; cursor:pointer;" onclick="prevMonth()">◀</button>
        <div id="month-name">มีนาคม 2569</div>
        <button style="border:none; background:none; cursor:pointer;" onclick="nextMonth()">▶</button>
    </div>
    
    <div class="weekdays">
        <div style="color: #e74c3c;">อา</div><div>จ</div><div>อ</div><div>พ</div><div>พฤ</div><div>ศ</div><div>ส</div>
    </div>
    
    <div class="days" id="calendar-days"></div>
</div>

<footer>
    สร้างสรรค์โดย: <b>เณรปลื้ม</b> 🙏<br>
    วัดสมุหเขตตาราม วัดหัววัง
</footer>

<div id="holyModal" class="modal">
    <div class="modal-content">
        <h2 style="color: var(--primary);">วันพระมหามงคล 🪷</h2>
        <p id="holy-detail"></p>
        <p style="font-style: italic; color: #777;">"ละเว้นความชั่ว ทำความดี ทำจิตใจให้บริสุทธิ์"</p>
        <button class="btn-close" onclick="closeModal()">รับทราบ</button>
    </div>
</div>

<script>
    // ข้อมูลวันพระ ปี 2569 (ตัวอย่าง)
    const holyData = {
        "2026-03-02": "วันมาฆบูชา (ขึ้น ๑๕ ค่ำ เดือน ๓)",
        "2026-03-08": "วันพระ (แรม ๘ ค่ำ เดือน ๓)",
        "2026-03-17": "วันพระ (แรม ๑๕ ค่ำ เดือน ๓)",
        "2026-03-25": "วันพระ (ขึ้น ๘ ค่ำ เดือน ๔)"
    };

    let currentDate = new Date(2026, 2, 1); // เริ่มที่ มีนาคม 2569

    function renderCalendar() {
        const daysContainer = document.getElementById('calendar-days');
        const monthName = document.getElementById('month-name');
        daysContainer.innerHTML = '';
        
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        monthName.innerText = new Intl.DateTimeFormat('th-TH', { month: 'long', year: 'numeric' }).format(currentDate);

        const firstDay = new Date(year, month, 1).getDay();
        const lastDate = new Date(year, month + 1, 0).getDate();

        for (let i = 0; i < firstDay; i++) {
            daysContainer.appendChild(document.createElement('div'));
        }

        for (let i = 1; i <= lastDate; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.classList.add('day');
            dayDiv.innerText = i;

            const dateStr = `${year}-${(month + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`;
            
            if (holyData[dateStr]) {
                dayDiv.classList.add('holy-day');
                dayDiv.onclick = () => showModal(holyData[dateStr]);
            }

            const today = new Date();
            if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayDiv.classList.add('today');
            }

            daysContainer.appendChild(dayDiv);
        }
    }

    function showModal(detail) {
        document.getElementById('holy-detail').innerText = detail;
        document.getElementById('holyModal').style.display = 'flex';
    }

    function closeModal() {
        document.getElementById('holyModal').style.display = 'none';
    }

    function prevMonth() { currentDate.setMonth(currentDate.getMonth() - 1); renderCalendar(); }
    function nextMonth() { currentDate.setMonth(currentDate.getMonth() + 1); renderCalendar(); }

    renderCalendar();
</script>

</body>
</html>
