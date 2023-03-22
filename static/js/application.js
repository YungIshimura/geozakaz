var dt = new DataTransfer();

$('.input-file input[type=file]').on('change', function(){
	let $files_list = $(this).closest('.input-file').next();
	$files_list.empty();

	for(var i = 0; i < this.files.length; i++){
		let new_file_input = '<div class="input-file-list-item">' +
			'<span class="input-file-list-name"> <svg width="28" height="33" viewBox="0 0 28 33" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M17.8501 1L27.1176 9.72913M27.1176 9.72913H19.5351C19.0882 9.72913 18.6596 9.56192 18.3436 9.26428C18.0276 8.96663 17.8501 8.56295 17.8501 8.14202V1H2.68501C2.23812 1 1.80953 1.16721 1.49353 1.46486C1.17753 1.7625 1 2.16619 1 2.58711V30.3616C1 30.7826 1.17753 31.1862 1.49353 31.4839C1.80953 31.7815 2.23812 31.9487 2.68501 31.9487H25.4326C25.8795 31.9487 26.3081 31.7815 26.6241 31.4839C26.9401 31.1862 27.1176 30.7826 27.1176 30.3616V9.72913Z" stroke="#2D9CDB" stroke-linecap="round" stroke-linejoin="round"/> </svg>' + this.files.item(i).name + '</span>' +
			'<a href="#" onclick="removeFilesItem(this); return false;" class="input-file-list-remove">x</a>' +
			'</div>';
		$files_list.append(new_file_input);
		dt.items.add(this.files.item(i));
	};
	this.files = dt.files;
});

function removeFilesItem(target){
	let name = $(target).prev().text();
	let input = $(target).closest('.input-file-row').find('input[type=file]');	
	$(target).closest('.input-file-list-item').remove();	
	for(let i = 0; i < dt.items.length; i++){
		if(name === dt.items[i].getAsFile().name){
			dt.items.remove(i);
		}
	}
	input[0].files = dt.files;  
}