# Copyright 2002-2004 FlatCap (Richard Russon)
# This file may be copied under the terms of the GNU Public License.
# http://www.gnu.org/licenses/gpl.html

Summary    : NTFS Kernel Module
Name       : %{name_suff}
Version    : %{version}
Release    : %{release}
Vendor     : Linux-NTFS Project
Source     : kernel-source-%{version}-%{release}.i386.rpm
Buildroot  : %{_tmppath}/%{name_bare}-root
Packager   : Richard Russon (FlatCap)
License    : GPL
Group      : System Environment/Kernel
Provides   : %{name_bare} = %{version}-%{release}
Provides   : %{name_suff} = %{version}-%{release}
Requires   : %{requires} = %{version}-%{release}
Requires   : %{requires_suff} = %{version}-%{release}
URL        : http://www.linux-ntfs.org/content/view/120/59/

%description
_______________________________________________________________________________

This RPM contains a binary Linux kernel module,
which provides read-only NTFS support.

Please read the NTFS FAQ if you want to know how to:

 * Mount an NTFS partition
 * Change the permissions/ownership of a mounted NTFS partition
 * Automatically mount an NTFS partition

FAQ: http://wiki.linux-ntfs.org/doku.php?id=faq
RPM: http://www.linux-ntfs.org/content/view/120/59/
SRC: http://www.linux-ntfs.org/content/view/128/64/
_______________________________________________________________________________

%install
rm -fr       $RPM_BUILD_ROOT
mkdir -p     $RPM_BUILD_ROOT/lib/modules/%{version}-%{release_suff}/kernel/fs/ntfs
cp %{module} $RPM_BUILD_ROOT/lib/modules/%{version}-%{release_suff}/kernel/fs/ntfs/%{module}
chmod 644    $RPM_BUILD_ROOT/lib/modules/%{version}-%{release_suff}/kernel/fs/ntfs/%{module}
touch        $RPM_BUILD_ROOT/lib/modules/%{version}-%{release_suff}/kernel/fs/ntfs/%{module}

%pre
#P=`uname -p`
#if [ "$P" != "unknown" ] && [ "$P" != "%{_target_cpu}" ]; then
#        echo "_______________________________________________________________________________"
#        echo
#        echo "ERROR: This is the wrong RPM."
#        echo
#        echo "You have an $P kernel installed, but this rpm is for an %{_target_cpu} processor."
#        echo
#        echo "The instructions on the linux-ntfs website will help you find the correct rpm."
#        echo
#        echo "  http://www.linux-ntfs.org/content/view/127/63/"
#        echo "_______________________________________________________________________________"
#        echo
#        exit 1
#fi

U=`uname -r`
VERREL=`echo $U | sed 's/smp\|BOOT\|bigmem$//'`
SUFFIX=`echo $U | sed 's/'$VERREL'//'`
[ "$SUFFIX" ] && SUFFIX="-$SUFFIX"

CURR_KRN=kernel$SUFFIX-$VERREL
REQU_KRN=%{requires_suff}-%{version}-%{release}

if [ $CURR_KRN != $REQU_KRN ]; then
        echo "_______________________________________________________________________________"
        echo
        echo "ERROR: This RPM cannot be installed yet."
        echo
        echo "This RPM requires $REQU_KRN."
        echo "You already have it installed, but it is not running."
        echo "Please reboot and select that kernel, then retry the install."
        echo "_______________________________________________________________________________"
        echo
        exit 1
fi

%post
EMAIL="rpm"
EMAIL=$EMAIL"@"
EMAIL=$EMAIL"flatcap"
EMAIL=$EMAIL"."
EMAIL=$EMAIL"org"
if [ ! -f $RPM_BUILD_ROOT/lib/modules/%{version}-%{release_suff}/kernel/fs/ntfs/%{module} ]; then
        echo "_______________________________________________________________________________"
        echo
        echo "ERROR: Cannot find the installed kernel module."
        echo
        echo "RPM: %{requires_suff}-%{version}-%{release}.%{_target_cpu}.rpm"
        echo
        echo "PLEASE: Report this error to $EMAIL"
        echo "_______________________________________________________________________________"
        echo
        exit 1
fi

if [ -f /boot/System.map-%{release_suff} ]; then
        /sbin/depmod -a -F /boot/System.map-%{release_suff} %{release_suff} || :
else
        /sbin/depmod -a || :
fi
if [ $? != 0 ]; then
        echo "_______________________________________________________________________________"
        echo
        echo "ERROR: Cannot update the module dependencies."
        echo
        echo "RPM: %{requires_suff}-%{version}-%{release}.%{_target_cpu}.rpm"
        echo
        echo "PLEASE: Report this error to $EMAIL"
        echo "_______________________________________________________________________________"
        echo
        exit 1
fi

/sbin/modprobe -q ntfs > /dev/null 2>&1
if [ $? != 0 ]; then
        echo "_______________________________________________________________________________"
        echo
        echo "ERROR: Cannot load the NTFS kernel module."
        echo
        echo "RPM: %{requires_suff}-%{version}-%{release}.%{_target_cpu}.rpm"
        echo
        echo "PLEASE: Report this error to $EMAIL"
        echo "_______________________________________________________________________________"
        echo
        exit 1
else
        rmmod ntfs
fi

echo "_______________________________________________________________________________"
echo
echo "The Linux NTFS RPM has been successfully installed."
echo
echo "Please read the NTFS FAQ if you want to know how to:"
echo
echo " * Mount an NTFS partition"
echo " * Change the permissions/ownership of a mounted NTFS partition"
echo " * Automatically mount an NTFS partition"
echo
echo "FAQ: http://wiki.linux-ntfs.org/doku.php?id=faq"
echo "RPM: http://www.linux-ntfs.org/content/view/120/59/"
echo "SRC: http://www.linux-ntfs.org/content/view/128/64/"
echo "_______________________________________________________________________________"
echo

%clean
rm -fr $RPM_BUILD_ROOT

%postun
if [ -f /boot/System.map-%{release_suff} ]; then
        /sbin/depmod -a -F /boot/System.map-%{release_suff} %{release_suff} || :
else
        /sbin/depmod -a || :
fi

%files
%defattr(0644,root,root,0755)
%dir /lib/modules/%{version}-%{release_suff}/kernel/fs/ntfs
/lib/modules/%{version}-%{release_suff}/kernel/fs/ntfs/%{module}

%changelog
* Tue Dec 06 2005 Richard Russon (FlatCap)
- Update links to new website

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

