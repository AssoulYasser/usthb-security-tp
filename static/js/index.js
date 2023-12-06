document.addEventListener(
    'DOMContentLoaded', () => {
        let addUserButton = document.getElementById('add_user_button') 
        let addUserDialog = document.getElementById('add_user_dialog')
        
        addUserButton.addEventListener('click', () => {
            console.log('abcd');
            addUserDialog.showModal() 
        })
    }
)