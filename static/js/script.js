const swiper = new Swiper('.swiper', {
   
    loop: true,

    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
    },

    // Navigation arrows
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});

document.addEventListener('DOMContentLoaded', function() {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
    });

    document.querySelectorAll('button.delete-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('data-url');
            const row = this.closest('tr'); // Find the closest table row

            swalWithBootstrapButtons.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'No, cancel!',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(url, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // CSRF token
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            row.remove(); // Remove the row from the table
                            swalWithBootstrapButtons.fire({
                                title: 'Deleted!',
                                text: 'Your file has been deleted.',
                                icon: 'success'
                            });
                        } else {
                            swalWithBootstrapButtons.fire({
                                title: 'Error!',
                                text: 'Something went wrong.',
                                icon: 'error'
                            });
                        }
                    })
                    .catch(error => {
                        swalWithBootstrapButtons.fire({
                            title: 'Error!',
                            text: 'Something went wrong.',
                            icon: 'error'
                        });
                    });
                } else if (result.dismiss === Swal.DismissReason.cancel) {
                    swalWithBootstrapButtons.fire({
                        title: 'Cancelled',
                        text: 'Your imaginary file is safe :)',
                        icon: 'error'
                    });
                }
            });
        });
    });
});





$(document).ready(function() {
    // Handle comment form submission
    $('.comment-form').on('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        
        var $form = $(this);
        var postId = $form.closest('.comment-card').data('post-id'); // Get the post ID
        var formData = $form.serialize();
        
        $.ajax({
            url: $form.attr('action'),
            type: 'POST',
            data: formData,
            success: function(response) {
                // Append the new comment to the comments section
                var newCommentHtml = response.html;
                $('#comments-' + postId).append(newCommentHtml); // Add new comment to the post
                
                // Clear the form textarea
                $form.find('textarea').val('');
                
                // Show success message
                Swal.fire({
                    title: 'Success!',
                    text: 'Comment added successfully!',
                    icon: 'success',
                    confirmButtonText: 'OK'
                });
            },
            error: function(xhr) {
                // Show error message
                Swal.fire({
                    title: 'Error!',
                    text: 'Error adding comment: ' + xhr.responseText,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });

    // Handle post delete
    $('.delete-comment-form[data-post-id]').on('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        
        var $form = $(this);
        var postId = $form.data('post-id');
        
        Swal.fire({
            title: 'Are you sure?',
            text: 'You won\'t be able to revert this!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#85d630',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: $form.attr('action'),
                    type: 'POST',
                    data: $form.serialize(),
                    success: function() {
                        $('#post-' + postId).remove(); // Remove post element
                        Swal.fire(
                            'Deleted!',
                            'Your post has been deleted.',
                            'success'
                        );
                    },
                    error: function(xhr) {
                        Swal.fire(
                            'Error!',
                            'Error deleting post: ' + xhr.responseText,
                            'error'
                        );
                    }
                });
            }
        });
    });

    // Handle comment delete
    $('.delete-comment-form[data-comment-id]').on('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        
        var $form = $(this);
        var commentId = $form.data('comment-id');
        
        Swal.fire({
            title: 'Are you sure?',
            text: 'You won\'t be able to revert this!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#85d630',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: $form.attr('action'),
                    type: 'POST',
                    data: $form.serialize(),
                    success: function() {
                        $('#comment-' + commentId).remove(); // Remove comment element
                        Swal.fire(
                            'Deleted!',
                            'Your comment has been deleted.',
                            'success'
                        );
                    },
                    error: function(xhr) {
                        Swal.fire(
                            'Error!',
                            'Error deleting comment: ' + xhr.responseText,
                            'error'
                        );
                    }
                });
            }
        });
    });
});