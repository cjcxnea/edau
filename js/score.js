document.addEventListener('DOMContentLoaded', async function() {
    let currentUser = null;

    const queryData = sessionStorage.getItem('queryData');
    
    if (queryData) {
        const { subject, uname, idNum } = JSON.parse(queryData);

        try {
            const response = await fetch('json/users-25(下).json');
            const data = await response.json();

            for (const user of data.users) {
                const subjectMatch = user.testSub === subject;
                const unameMatch = user.uname === uname;
                const idNumMatch = user.idCard === idNum || user.examNum === idNum;

                if (subjectMatch && unameMatch && idNumMatch) {
                    currentUser = user;
                    break;
                }
            }
        } catch (error) {
            console.error('加载数据失败:', error);
            alert('加载数据失败，请稍后重试');
            window.location.href = 'v1.html';
            return;
        }
    }

    if (!currentUser) {
        alert('页面加载失败：未获取到用户信息');
        window.location.href = 'v1.html';
        return;
    }

    document.getElementById('test-sub').textContent = currentUser.testSub || '';
    document.getElementById('user-name').textContent = currentUser.uname || '';
    document.getElementById('user-idcard').textContent = currentUser.idCard || '';
    document.getElementById('user-school').textContent = currentUser.schoolName || '';
    document.getElementById('user-report-num').textContent = currentUser.reportNum || '';

    document.getElementById('score-exam-num').textContent = currentUser.examNum || '';
    document.getElementById('score-total').textContent = currentUser.totalScore || '';
    document.getElementById('score-listening').textContent = currentUser.listening || '';
    document.getElementById('score-reading').textContent = currentUser.reading || '';
    document.getElementById('score-writing').textContent = currentUser.writing || '';
    document.getElementById('speaking-exam-num').textContent = currentUser.speakingExamNum || '';
    document.getElementById('speaking-score').textContent = currentUser.speakingScore || '';

    const nameElement = document.querySelector('.user-info li:nth-child(1) .user-info-value');
    const idCardElement = document.querySelector('.user-info li:nth-child(2) .user-info-value');

    function maskName(name) {
        if (!name || name.length <= 1) return name || '';
        return name.charAt(0) + '*'.repeat(name.length - 1);
    }

    function maskIdCard(idCard) {
        if (!idCard || idCard.length < 5) return idCard || '';
        const middleLength = idCard.length - 2 - 3;
        return idCard.substring(0, 2) + '*'.repeat(middleLength) + idCard.substring(idCard.length - 3);
    }

    if (nameElement) {
        nameElement.textContent = maskName(nameElement.textContent);
    }
    if (idCardElement) {
        idCardElement.textContent = maskIdCard(idCardElement.textContent);
    }

    if (currentUser.reportNum === '0') {
        const reportNumElement = document.querySelector('.user-info li:nth-child(4)');
        if (reportNumElement) {
            reportNumElement.style.display = 'none';
        }
    }

    const backButton = document.querySelector('.btn button');
    if (backButton) {
        backButton.addEventListener('click', function() {
            sessionStorage.removeItem('queryData');
            window.location.href = 'v1.html';
        });
    }
});
