# Copyright 2002-2004 FlatCap (Richard Russon)
# This file may be copied under the terms of the GNU Public License.
# http://www.gnu.org/licenses/gpl.html

Summary    : NTFS Kernel Module
Name       : kernel-module-ntfs-%{uname}
Epoch      : %{epoch}
Version    : %{version}
Release    : %{release}
Vendor     : Linux-NTFS Project
Buildroot  : %{_tmppath}/kernel-module-ntfs-root
Packager   : Richard Russon (FlatCap)
License    : GPL
Group      : System Environment/Kernel
Provides   : kernel-module-ntfs = %{epoch}:%{version}-%{release}
Provides   : kernel-module
URL        : http://www.linux-ntfs.org/content/view/120/59/

%description
_______________________________________________________________________________

This RPM contains a binary Linux kernel module,
which provides safe, read-only, NTFS support.

Please read the NTFS FAQ if you want to know how to:

 * Mount an NTFS partition
 * Change the permissions/ownership of a mounted NTFS partition
 * Automatically mount an NTFS partition

FAQ: http://wiki.linux-ntfs.org/doku.php?id=faq
RPM: http://www.linux-ntfs.org/content/view/120/59/
SRC: http://www.linux-ntfs.org/content/view/128/64/
_______________________________________________________________________________

%install
rm -fr     $RPM_BUILD_ROOT
mkdir -p   $RPM_BUILD_ROOT/lib/modules/%{uname}/kernel/fs/ntfs
cp ntfs.ko $RPM_BUILD_ROOT/lib/modules/%{uname}/kernel/fs/ntfs/ntfs.ko
chmod 644  $RPM_BUILD_ROOT/lib/modules/%{uname}/kernel/fs/ntfs/ntfs.ko
touch      $RPM_BUILD_ROOT/lib/modules/%{uname}/kernel/fs/ntfs/ntfs.ko

%pre

%post
if [ -f /boot/System.map-%{uname} ]; then
        /sbin/depmod -a -F /boot/System.map-%{uname} %{uname} || :
else
        /sbin/depmod -a || :
fi

%clean
rm -fr $RPM_BUILD_ROOT

%postun
if [ -f /boot/System.map-%{uname} ]; then
        /sbin/depmod -a -F /boot/System.map-%{uname} %{uname} || :
else
        /sbin/depmod -a || :
fi

%files
%defattr(0644,root,root,0755)
%dir /lib/modules/%{uname}/kernel/fs/ntfs
/lib/modules/%{uname}/kernel/fs/ntfs/ntfs.ko

%changelog
* Tue Dec 06 2005 Richard Russon (FlatCap)
- Update links to new website

* Sun Oct 17 2004 Richard Russon (FlatCap)
- Change the naming convention to kernel-module-ntfs
- Quieten down the rpm

* Sun Mar 21 2004 Richard Russon (FlatCap)
- Obfuscate my email address

* Sun Feb 01 2004 Richard Russon (FlatCap)
- Fix the error messages to give the rpm name

* Tue Jan 22 2004 Richard Russon (FlatCap)
- Prevent people from installing the i386 version

* Sun Nov 09 2003 Richard Russon (FlatCap)
- Finally finished rpm overhaul

* Tue Sep 23 2003 Richard Russon (FlatCap)
- Make depmod stage smarter

* Mon Aug 20 2003 Richard Russon (FlatCap)
- Updated build script and spec file

* Fri Jul 18 2003 Richard Russon (FlatCap)
- Finally got my hands on 2.4.20-6
- Thanks to Rob Lee

* Thu Apr 03 2003 Richard Russon (FlatCap)
- New kernel release - Thanks to fugimax

* Sun Dec 22 2002 Richard Russon (FlatCap)
- Simplified install

* Tue Nov 19 2002 Richard Russon (FlatCap)
- Made (un)install smarter
- Thanks to John Interrante

* Sun Nov 17 2002 Richard Russon (FlatCap)
- Removed RedHat codename from description
- Simplified depmod

* Wed Oct 30 2002 Richard Russon (FlatCap)
- Fix the SMP RPMs

* Mon Oct 28 2002 Richard Russon (FlatCap)
- Added SMP modules

* Sun Oct 20 2002 Richard Russon (FlatCap)
- More arches, untested

* Tue Oct 15 2002 Richard Russon (FlatCap)
- First release of ntfs driver for Redhat 8.0

