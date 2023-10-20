rpmbuild --define "_topdir %(pwd)/rpmbuild" --define "buildroot %(pwd)/rpmbuild/BUILDROOT" -bb cnx-freeswitch.spec
