document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const subjectSelect = document.getElementById('subject');
    const unameInput = document.getElementById('uname');
    const idNumInput = document.getElementById('idNum');
    const submitButton = document.querySelector('.btn button');

    submitButton.addEventListener('click', async function(e) {
        e.preventDefault();

        const selectedSubjectValue = subjectSelect.value;
        const selectedSubjectText = subjectSelect.options[subjectSelect.selectedIndex].text;
        const uname = unameInput.value.trim();
        const idNum = idNumInput.value.trim();

        if (!selectedSubjectValue || !uname || !idNum) {
            alert('请填写完整信息');
            return;
        }

        try {
            const response = await fetch('json/users-25(下).json');
            const data = await response.json();

            let matchedUser = null;

            for (const user of data.users) {
                const subjectMatch = user.testSub === selectedSubjectText;
                const unameMatch = user.uname === uname;
                const idNumMatch = user.idCard === idNum || user.examNum === idNum;

                if (subjectMatch && unameMatch && idNumMatch) {
                    matchedUser = user;
                    break;
                }
            }

            if (matchedUser) {
                sessionStorage.setItem('queryData', JSON.stringify({
                    subject: selectedSubjectText,
                    uname: uname,
                    idNum: idNum
                }));
                window.location.href = 'score.html';
            } else {
                alert('请输入正确的信息');
            }
        } catch (error) {
            console.error('加载数据失败:', error);
            alert('加载数据失败，请稍后重试');
        }
    });
});
