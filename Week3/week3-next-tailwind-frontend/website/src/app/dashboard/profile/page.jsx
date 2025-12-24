export default function ProfilePage() {
  return (
    <div className="min-h-screen bg-grey-50 flex justify-center items-start py-12">

      {/* PROFILE CARD */}
      <div className="bg-white w-full max-w-4xl rounded-sm shadow-md p-6">

        {/* GO BACK */}
        <a
          href="/dashboard"
          className="text-sm text-blue-500 hover:underline mb-4 inline-block"
        >
          ← Go back
        </a>

        {/* TOP SECTION */}
        <div className="flex gap-6 border-b pb-6">

          {/* PROFILE IMAGE */}
          <img
            src="https://randomuser.me/api/portraits/women/44.jpg"
            alt="Profile"
            className="w-32 h-32 object-cover rounded-sm"
          />

          {/* DETAILS GRID */}
          <div className="flex-1 grid grid-cols-2 gap-x-8 gap-y-4 text-sm">

            <div>
              <p className="text-gray-400">Name</p>
              <p className="text-gray-900">Nina Valentine</p>
            </div>

            <div>
              <p className="text-gray-400">LinkedIn</p>
              <a className="text-blue-500" href="#">
                linkedin.com
              </a>
            </div>

            <div>
              <p className="text-gray-400">Job Title</p>
              <p className="text-gray-900">Actress</p>
            </div>

            <div>
              <p className="text-gray-400">Twitter</p>
              <a className="text-blue-500" href="#">
                www.x.com
              </a>
            </div>

            <div>
              <p className="text-gray-400">Email</p>
              <a className="text-blue-500" href="#">
                nina_val@example.com
              </a>
            </div>

            <div>
              <p className="text-gray-400">Facebook</p>
              <a className="text-blue-500" href="#">
                facebook.com
              </a>
            </div>
          </div>
        </div>

        {/* BIO */}
        <div className="pt-6 text-sm">
          <p className="text-gray-400 mb-1">Bio</p>
          <p className="text-gray-600 leading-relaxed">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent
            aliquet odio augue, in dapibus lacus imperdiet ut. Quisque elementum
            placerat neque rhoncus tempus. Cras id suscipit diam, sit amet
            rutrum ipsum. Vestibulum rutrum elit lacinia sapien porta pulvinar.
          </p>
        </div>

        {/* EDIT PROFILE */}
        <div className="pt-6">
          <a href="#" className="text-blue-500 text-sm hover:underline">
            Edit Profile
          </a>
        </div>
      </div>
    </div>
  );
}
