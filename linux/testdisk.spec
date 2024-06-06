%define ver_progsreiserfs 0.3.1-rc8
#% define is_wip 1
%{?is_wip:%define ver_wip -WIP}

Summary:	Tool to check and undelete partition, PhotoRec recovers lost files
Summary(pl.UTF8):	Narzędzie sprawdzające i odzyskujące partycje
Summary(fr.UTF8):	Outil pour vérifier et restaurer des partitions
Summary(ru_RU.UTF8): Программа для проверки и восстановления разделов диска
Name:		testdisk
Version:	7.2
Release:	1%{?dist}
License:	GPLv2+
Source0:	https://www.cgsecurity.org/testdisk-%{version}%{?ver_wip}.tar.bz2
Source1:	progsreiserfs-%ver_progsreiserfs.tar.gz
Patch0:		progsreiserfs-journal.patch
Patch1:		progsreiserfs-file-read.patch
URL:		https://www.cgsecurity.org/wiki/TestDisk
BuildRequires:	desktop-file-utils
BuildRequires:	e2fsprogs-devel
BuildRequires:	make
BuildRequires:	libewf-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libuuid-devel
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	ntfs-3g-devel
BuildRequires:  qt5-linguist
BuildRequires:	qt5-qtbase-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes:	testdisk-doc < 6.12
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
Tool to check and undelete partition. Works with FAT12, FAT16, FAT32,
NTFS, ext2, ext3, ext4, btrfs, BeFS, CramFS, HFS, JFS, Linux Raid, Linux
Swap, LVM, LVM2, NSS, ReiserFS, UFS, XFS.
PhotoRec is a signature based file recovery utility. It handles more than
440 file formats including JPG, MSOffice, OpenOffice documents.

%description -l pl.UTF8
Narzędzie sprawdzające i odzyskujące partycje. Pracuje z partycjami:
FAT12, FAT16, FAT32, NTFS, ext2, ext3, ext4, btrfs, BeFS, CramFS, HFS, JFS,
Linux Raid, Linux Swap, LVM, LVM2, NSS, ReiserFS, UFS, XFS.
PhotoRec is a signature based file recovery utility. It handles more than
440 file formats including JPG, MSOffice, OpenOffice documents.

%description -l fr.UTF8
TestDisk vérifie et récupère les partitions. Fonctionne avec
FAT12, FAT16, FAT32, NTFS, ext2, ext3, ext4, btrfs, BeFS, CramFS, HFS, JFS,
Linux Raid, Linux Swap, LVM, LVM2, NSS, ReiserFS, UFS, XFS.
PhotoRec utilise un mécanisme de signature pour récupérer des fichiers perdus.
Il reconnait plus de 440 de formats de fichiers dont les JPEG,
les documents MSOffice ou OpenOffice.

%description -l ru_RU.UTF8
Программа для проверки и восстановления разделов диска.
Поддерживает следующие типы разделов:
FAT12, FAT16, FAT32, NTFS, ext2, ext3, ext4, btrfs, BeFS, CramFS, HFS, JFS,
Linux Raid, Linux Swap, LVM, LVM2, NSS, ReiserFS, UFS, XFS.
PhotoRec is a signature based file recovery utility. It handles more than
440 file formats including JPG, MSOffice, OpenOffice documents.

%package -n qphotorec
Summary:	Signature based file carver. Recover lost files

%description -n qphotorec
QPhotoRec is a Qt version of PhotoRec. It is a signature based file recovery
utility. It handles more than 440 file formats including JPG, MSOffice,
OpenOffice documents.


%prep
%setup -q -n %{name}-%{version}%{?ver_wip}
%setup -q -a 1 -D -n %{name}-%{version}%{?ver_wip}
%patch0
%patch1

%build
(
cd progsreiserfs-%ver_progsreiserfs
%configure --disable-Werror
make
)
%configure \
 --with-reiserfs-lib=${RPM_BUILD_DIR}/%{name}-%{version}/progsreiserfs-%ver_progsreiserfs/libreiserfs/.libs/ 	\
 --with-reiserfs-includes=${RPM_BUILD_DIR}/%{name}-%{version}/progsreiserfs-%ver_progsreiserfs/include/ 	\
 --with-dal-lib=${RPM_BUILD_DIR}/%{name}-%{version}/progsreiserfs-%ver_progsreiserfs/libdal/.libs/		\
 --docdir=%{_pkgdocdir}
make %{?_smp_mflags}
%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

%clean
rm -rf $RPM_BUILD_ROOT

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/qphotorec.desktop

%post -n qphotorec
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n qphotorec
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n qphotorec
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc AUTHORS ChangeLog NEWS README.md THANKS
%license COPYING
%{_bindir}/fidentify
%{_bindir}/photorec
%{_bindir}/testdisk
%{_mandir}/man8/fidentify.8*
%{_mandir}/man8/photorec.8*
%{_mandir}/man8/testdisk.8*
%{_mandir}/zh_CN/man8/fidentify.8*
%{_mandir}/zh_CN/man8/photorec.8*
%{_mandir}/zh_CN/man8/testdisk.8*

%files -n qphotorec
%{_bindir}/qphotorec
%{_mandir}/man8/qphotorec.8*
%{_mandir}/zh_CN/man8/qphotorec.8*
%{_datadir}/applications/qphotorec.desktop
%{_datadir}/icons/hicolor/48x48/apps/qphotorec.png
%{_datadir}/icons/hicolor/scalable/apps/qphotorec.svg

%changelog
* Wed May 11 2011 Christophe Grenier <grenier@cgsecurity.org> 6.12-0
- 6.12

* Thu Jul 17 2008 Christophe Grenier <grenier@cgsecurity.org> 6.10-1
- 6.10

* Sun Jan 4 2004 Christophe Grenier <grenier@cgsecurity.org> 5.0
- 5.0

* Wed Oct 1 2003 Christophe Grenier <grenier@cgsecurity.org> 4.5
- 4.5

* Wed Apr 23 2003 Christophe Grenier <grenier@cgsecurity.org> 4.4-2

* Sat Mar 29 2003 Pascal Terjan <CMoi@tuxfamily.org> 4.4-1mdk
- 4.4

* Fri Dec 27 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.2-2mdk
- rebuild for rpm and glibc

* Sun Oct 06 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.2-1mdk
- 4.2

* Mon Sep 02 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.1-1mdk 
- By Pascal Terjan <pascal.terjan@free.fr>
	- first mdk release, adapted from PLD.
	- gz to bz2 compression.
- fix %%tmppath
- %%make instead %%{__make}
