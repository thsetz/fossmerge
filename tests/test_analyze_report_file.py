import os
import pprint
from fossmerge import analyze_docx_file


def test_that_the_fixture_returns_an_existing_file(docx_report_file):
    assert os.path.exists(docx_report_file)


def test_that_the_state_xml_file_is_analyzed_as_expected(docx_report_file):
    ds = analyze_docx_file.convert_and_analyze_docx(docx_report_file)
    tables = analyze_docx_file.AVAILABLE_TABLES
    assert ds.keys() == tables.keys()
    assert tables["FIRST"]["ROWS"] == [
        ["OSS Component Clearing report"],
        ["Clearing Information", "Department", "FOSSology Generation"],
        ["Prepared by", "2019/10/16 siddarth.hs@siemens.com (CT BE)"],
        ["Reviewed by (opt.)", "2019/10/16 anju.john@siemens.com (CT BE)"],
        ["Report release date", "NA"],
        ["Component Information", "Community", "NA"],
        ["Component", "zlib"],
        ["Version", "1.2.11"],
        ["Component hash (SHA-1)", "11196A78B14DDBCF82FA9E4ADD00F76323E93345"],
        ["Release date", "NA"],
        ["Main license(s)", "Zlib."],
        ["", "Other license(s)", "Info-ZIP, Public-domain."],
        [
            "",
            "Fossology Upload/Package Link",
            "https://fossology.siemens.com/repo/?mod=showjobs&upload=19716",
        ],
        [
            "",
            "SW360 Portal Link",
            "https://sw360.siemens.com/group/guest/components/-/component/release/detailRelease/7f75885d309970833f4187295dc54718",
        ],
        [
            "",
            "Result of License Scan",
            "GPL, Info-ZIP, No_license_found, Perl-possibility, Public-domain, "
            "See-doc.OTHER, UnclassifiedLicense, Zlib, Zlib-possibility.",
        ],
    ]
    assert tables["assessment-summary"]["ROWS"] == [
        [
            "General assessment",
            "The global license of this component is licensed under Zlib Licence. Only "
            "common rules apply for this component.\n"
            "This clearing is for combined source package which includes the debian "
            "modifications/extensions to the original/upstream source from the OSS "
            "project.",
        ],
        ["", ""],
        [
            "Source / binary integration notes",
            "1 no critical files found, source code and binaries can be used as is\n"
            "critical files found, source code needs to be adapted and binaries possibly "
            "re-built",
        ],
        [
            "Dependency notes",
            "1 no dependencies found, neither in source code nor in binaries\n"
            "dependencies found in source code (see obligations)\n"
            "dependencies found in binaries (see obligations)",
        ],
        [
            "Export restrictions by copyright owner",
            "1 no export restrictions found\n"
            "export restrictions found (see obligations)",
        ],
        [
            "Restrictions for use (e.g. not for Nuclear Power) by copyright owner",
            "1 no restrictions for use found\n"
            "restrictions for use found (see obligations)",
        ],
        ["Additional notes", "NA"],
        ["General Risks (optional)", "NA"],
    ]
    assert tables["required-license-compliance-tasks"]["ROWS"] == []
    assert tables["common-obligations-restrictions-and-risks"]["ROWS"] == [
        [
            "2.1.1",
            "Documentation of license conditions and copyright notices in product "
            "documentation (License Notice File / README_OSS) is provided by this "
            "component clearing report:",
        ],
        [
            "",
            "1.a All relevant licenses (global and others - see below) must be added to "
            "the legal approved Readme_OSS template. Remark: “Do Not Use” licenses must "
            "not be added to the ReadMe_OSS\n"
            "\n"
            "\n"
            "1.b Add all copyrights to README_OSS\n"
            "\n"
            "\n"
            "1.c Add all relevant acknowledgements to Readme_OSS",
        ],
        [
            "2.1.2",
            "Additional Common Obligations:\n"
            "\n"
            "\n"
            "Need to be ensured by the distributing party:",
        ],
        [
            "",
            "2 Modifications in Source Code\n"
            "\n"
            "\n"
            "If modifications are permitted:\n"
            "\n"
            "\n"
            "2.a Do not change or delete Copyright, patent, trademark, attribution "
            "notices or any further legal notices or license texts in any files - i.e. "
            "neither within any source file of the component package nor in any of its "
            "documentation files.\n"
            "\n"
            "\n"
            "2.b Document all changes and modifications in source code files with "
            "copyright notices:\n"
            "\n"
            "\n"
            "Add copyright (including company and date), function, reason for "
            "modification in the header.\n"
            "\n"
            "\n"
            "Example:\n"
            "\n"
            "\n"
            "© Siemens AG, 2013\n"
            "\n"
            "\n"
            "March 18th, 2013 Modified helloworld() – fix memory leak\n"
            "\n"
            "\n"
            "3 Obligations and risk assessment regarding distribution\n"
            "\n"
            "\n"
            "3.a Ensure that your distribution terms which are agreed with Siemens’ "
            "customers (e.g. standard terms, “AGB”, or individual agreements) define "
            "that the open source license conditions shall prevail over the Siemens’ "
            "license conditions with respect to the open source software (usually this "
            "is part of Readme OSS).\n"
            "\n"
            "\n"
            "3.b Do not use any names, trademarks, service marks or product names of the "
            "author(s) and/or licensors to endorse or promote products derived from this "
            "software component without the prior written consent of the author(s) "
            "and/or the owner of such rights.\n"
            "\n"
            "\n"
            "3.c Add a statement to the README_OSS that the OSS portions of this Product "
            "are provided royalty-free and can be used at no charge",
        ],
        ["2.1.3", "Obligations and risk assessment regarding distribution"],
        ["", ""],
    ]
    assert tables["additional-obligations-restrictions-risks-beyond-common-rules"][
        "ROWS"
    ] == [
        ["Obligation", "License", "License section reference and short Description"],
        ["", "", ""],
    ]
    assert tables["acknowledgements"]["ROWS"] == [["", "", ""]]
    assert tables["export-restrictions"]["ROWS"] == [["", "", ""]]
    assert tables["intellectual-property"]["ROWS"] == [["", "", ""]]
    assert tables["notes"]["ROWS"] == []
    assert tables["notes-on-individual-files"]["ROWS"] == [["", "", ""]]
    assert tables["results-of-license-scan"]["ROWS"] == [
        ["1", "0", "GPL"],
        ["1", "1", "Info-ZIP"],
        ["106", "0", "No_license_found"],
        ["1", "0", "Perl-possibility"],
        ["3", "3", "Public-domain"],
        ["1", "0", "See-doc.OTHER"],
        ["1", "0", "UnclassifiedLicense"],
        ["11", "43", "Zlib"],
        ["33", "0", "Zlib-possibility"],
    ]
    assert tables["main-licenses"]["ROWS"] == [
        [
            "Zlib",
            "This software is provided 'as-is', without any express or implied warranty. "
            "In no event will the authors be held liable for any damages arising from "
            "the use of this software.\n"
            "\n"
            "Permission is granted to anyone to use this software for any purpose, "
            "including commercial applications, and to alter it and redistribute it "
            "freely, subject to the following restrictions:\n"
            "\n"
            "1. The origin of this software must not be misrepresented; you must not "
            "claim that you wrote the original software. If you use this software in a "
            "product, an acknowledgment in the product documentation would be "
            "appreciated but is not required.\n"
            "\n"
            "2. Altered source versions must be plainly marked as such, and must not be "
            "misrepresented as being the original software.\n"
            "\n"
            "3. This notice may not be removed or altered from any source distribution.",
            "Makefile.in\n"
            "\n"
            "\n"
            "README\n"
            "\n"
            "\n"
            "adler32.c\n"
            "\n"
            "\n"
            "compress.c\n"
            "\n"
            "\n"
            "contrib/minizip/unzip.h\n"
            "\n"
            "\n"
            "contrib/minizip/zip.h\n"
            "\n"
            "\n"
            "crc32.c\n"
            "\n"
            "\n"
            "debian/copyright\n"
            "\n"
            "\n"
            "deflate.c\n"
            "\n"
            "\n"
            "deflate.h\n"
            "\n"
            "\n"
            "examples/gun.c\n"
            "\n"
            "\n"
            "examples/gzappend.c\n"
            "\n"
            "\n"
            "examples/gzjoin.c\n"
            "\n"
            "\n"
            "examples/gzlog.c\n"
            "\n"
            "\n"
            "examples/gzlog.h\n"
            "\n"
            "\n"
            "examples/zran.c\n"
            "\n"
            "\n"
            "gzclose.c\n"
            "\n"
            "\n"
            "gzguts.h\n"
            "\n"
            "\n"
            "gzlib.c\n"
            "\n"
            "\n"
            "gzread.c\n"
            "\n"
            "\n"
            "gzwrite.c\n"
            "\n"
            "\n"
            "infback.c\n"
            "\n"
            "\n"
            "inffast.c\n"
            "\n"
            "\n"
            "inffast.h\n"
            "\n"
            "\n"
            "inflate.c\n"
            "\n"
            "\n"
            "inflate.h\n"
            "\n"
            "\n"
            "inftrees.c\n"
            "\n"
            "\n"
            "inftrees.h\n"
            "\n"
            "\n"
            "msdos/Makefile.dj2\n"
            "\n"
            "\n"
            "msdos/Makefile.emx\n"
            "\n"
            "\n"
            "old/Makefile.emx\n"
            "\n"
            "\n"
            "old/os2/Makefile.os2\n"
            "\n"
            "\n"
            "test/example.c\n"
            "\n"
            "\n"
            "test/infcover.c\n"
            "\n"
            "\n"
            "test/minigzip.c\n"
            "\n"
            "\n"
            "trees.c\n"
            "\n"
            "\n"
            "uncompr.c\n"
            "\n"
            "\n"
            "zconf.h\n"
            "\n"
            "\n"
            "zconf.h.cmakein\n"
            "\n"
            "\n"
            "zconf.h.in\n"
            "\n"
            "\n"
            "zlib.h\n"
            "\n"
            "\n"
            "zutil.c\n"
            "\n"
            "\n"
            "zutil.h",
        ]
    ]

    assert tables["other-oss-licenses-red---do-not-use-licenses"]["ROWS"] == [
        ["", "", ""]
    ]
    assert tables[
        "other-oss-licenses-yellow---additional-obligations-to-common-rules-e.g.-copyleft"
    ]["ROWS"] == [["", "", ""]]
    assert tables["other-oss-licenses-white---only-common-rules"]["ROWS"] == [
        [
            "Info-ZIP",
            'For the purposes of this copyright and license, "Info-ZIP" is defined as '
            "the following set of individuals:\n"
            "\n"
            "Mark Adler, John Bush, Karl Davis, Harald Denker, Jean-Michel Dubois, "
            "Jean-loup Gailly, Hunter Goatley, Ed Gordon, Ian Gorman, Chris Herborth, "
            "Dirk Haase, Greg Hartwig, Robert Heath, Jonathan Hudson, Paul Kienitz, "
            "David Kirschbaum, Johnny Lee, Onno van der Linden, Igor Mandrichenko, Steve "
            "P. Miller, Sergio Monesi, Keith Owens, George Petrov, Greg Roelofs, Kai Uwe "
            "Rommel, Steve Salisbury, Dave Smith, Steven M. Schweda, Christian Spieler, "
            "Cosmin Truta, Antoine Verheijen, Paul von Behren, Rich Wales, Mike White.\n"
            "\n"
            'This software is provided "as is," without warranty of any kind, express or '
            "implied. In no event shall Info-ZIP or its contributors be held liable for "
            "any direct, indirect, incidental, special or consequential damages arising "
            "out of the use of or inability to use this software.\n"
            "\n"
            "Permission is granted to anyone to use this software for any purpose, "
            "including commercial applications, and to alter it and redistribute it "
            "freely, subject to the above disclaimer and the following restrictions:\n"
            "\n"
            "* Redistributions of source code (in whole or in part) must retain the "
            "above copyright notice, definition, disclaimer, and this list of "
            "conditions.\n"
            "\n"
            "* Redistributions in binary form (compiled executables and libraries) must "
            "reproduce the above copyright notice, definition, disclaimer, and this list "
            "of conditions in documentation and/or other materials provided with the "
            "distribution. Additional documentation is not needed for executables where "
            "a command line license option provides these and a note regarding this "
            "option is in the executable's startup banner. The sole exception to this "
            "condition is redistribution of a standard UnZipSFX binary (including "
            "SFXWiz) as part of a self-extracting archive; that is permitted without "
            "inclusion of this license, as long as the normal SFX banner has not been "
            "removed from the binary or disabled.\n"
            "\n"
            "* Altered versions--including, but not limited to, ports to new operating "
            "systems, existing ports with new graphical interfaces, versions with "
            "modified or added functionality, and dynamic, shared, or static library "
            "versions not from Info-ZIP--must be plainly marked as such and must not be "
            "misrepresented as being the original source or, if binaries, compiled from "
            "the original source. Such altered versions also must not be misrepresented "
            "as being Info-ZIP releases--including, but not limited to, labeling of the "
            'altered versions with the names "Info-ZIP" (or any variation thereof, '
            'including, but not limited to, different capitalizations), "Pocket UnZip," '
            '"WiZ" or "MacZip" without the explicit permission of Info-ZIP. Such altered '
            "versions are further prohibited from misrepresentative use of the Zip-Bugs "
            "or Info-ZIP e-mail addresses or the Info-ZIP URL(s), such as to imply "
            "Info-ZIP will provide support for the altered versions.\n"
            "\n"
            '* Info-ZIP retains the right to use the names "Info-ZIP," "Zip," "UnZip," '
            '"UnZipSFX," "WiZ," "Pocket UnZip," "Pocket Zip," and "MacZip" for its own '
            "source and binary releases.",
            "contrib/minizip/unzip.c",
        ],
        [
            "Public-domain",
            "Not copyrighted -- provided to the public domain",
            "examples/fitblk.c\n\n\nexamples/zlib_how.html\n\n\nexamples/zpipe.c",
        ],
    ]
    assert tables["overview-of-all-licenses-with-or-without-obligations"]["ROWS"] == [
        ["Info-ZIP", ""]
    ]
    assert tables["copyrights"]["ROWS"] == [
        ["Copyright: 2000-2017 Mark Brown", "", "debian/copyright"],
        [
            "Copyright: 1998-2010 Gilles Vollant 2007-2008 Even Rouault 2009-2010 "
            "Mathias Svensson",
            "",
            "debian/copyright",
        ],
        ["Copyright: 1998 by Andreas R. Kleinert", "", "debian/copyright"],
        [
            "Copyright: 1995-2013 Jean-loup Gailly and Mark Adler",
            "",
            "debian/copyright",
        ],
        [
            "Copyright Jean-loup Gailly Osma Ahvenlampi <Osma.Ahvenlampi@hut.fi> Amiga",
            "",
            "amiga/Makefile.sas",
        ],
        [
            "Copyright 1998-2004 Gilles Vollant - http://www.winimage.com/zLibDll",
            "",
            "contrib/minizip/unzip.c\n\n\ncontrib/minizip/zip.c",
        ],
        ["Copyright 1995-2017 Mark Adler", "", "inftrees.c"],
        ["Copyright 1995-2017 Jean-loup Gailly and Mark Adler", "", "deflate.c"],
        ["Copyright (c) 2004, 2005 by Mark Adler", "", "examples/zlib_how.html"],
        ["Copyright (c) 2004, 2005 Mark Adler", "", "examples/zlib_how.html"],
        [
            "Copyright (c) 1998-2010 - by Gilles Vollant - version 1.1 64 bits from "
            "Mathias Svensson",
            "",
            "contrib/minizip/MiniZip64_info.txt",
        ],
        [
            "Copyright (c) 1990-2000 Info-ZIP. All rights reserved.",
            "",
            "contrib/minizip/unzip.c",
        ],
        ["Copyright (C) 2011, 2016 Mark Adler", "", "test/infcover.c"],
        [
            "Copyright (C) 2009-2010 Mathias Svensson ( http://result42.com )",
            "",
            "contrib/minizip/ioapi.c\n"
            "\n"
            "\n"
            "contrib/minizip/ioapi.h\n"
            "\n"
            "\n"
            "contrib/minizip/iowin32.c\n"
            "\n"
            "\n"
            "contrib/minizip/iowin32.h\n"
            "\n"
            "\n"
            "contrib/minizip/miniunz.c\n"
            "\n"
            "\n"
            "contrib/minizip/minizip.c\n"
            "\n"
            "\n"
            "contrib/minizip/unzip.c\n"
            "\n"
            "\n"
            "contrib/minizip/unzip.h\n"
            "\n"
            "\n"
            "contrib/minizip/zip.c\n"
            "\n"
            "\n"
            "contrib/minizip/zip.h",
        ],
        [
            "Copyright (C) 2007-2008 Even Rouault",
            "",
            "contrib/minizip/miniunz.c\n"
            "\n"
            "\n"
            "contrib/minizip/minizip.c\n"
            "\n"
            "\n"
            "contrib/minizip/unzip.c\n"
            "\n"
            "\n"
            "contrib/minizip/unzip.h",
        ],
        ["Copyright (C) 2007, 2008, 2012 Mark Adler", "", "examples/enough.c"],
        ["Copyright (C) 2005, 2012 Mark Adler", "", "examples/zran.c"],
        ["Copyright (C) 2004-2017 Mark Adler", "", "gzlib.c\n\n\ngzwrite.c"],
        ["Copyright (C) 2004, 2010 Mark Adler", "", "gzclose.c"],
        [
            "Copyright (C) 2004, 2008, 2012, 2016 Mark Adler, all rights reserved",
            "",
            "examples/gzlog.c",
        ],
        ["Copyright (C) 2004, 2008, 2012 Mark Adler", "", "examples/gzlog.h"],
        [
            "Copyright (C) 2004, 2005, 2012 Mark Adler, all rights reserved",
            "",
            "examples/gzjoin.c",
        ],
        [
            "Copyright (C) 2004, 2005, 2010, 2011, 2012, 2013, 2016 Mark Adler",
            "",
            "gzguts.h\n\n\ngzread.c",
        ],
        ["Copyright (C) 2003-2010 Mark Adler", "", "examples/gun.c"],
        [
            "Copyright (C) 2003, 2012 Mark Adler, all rights reserved",
            "",
            "examples/gzappend.c",
        ],
        ["Copyright (C) 2003, 2012 Mark Adler", "", "examples/gzappend.c"],
        ["Copyright (C) 2003, 2005, 2008, 2010, 2012 Mark Adler", "", "examples/gun.c"],
        [
            "Copyright (C) 1998-2010 Gilles Vollant (minizip) ( "
            "http://www.winimage.com/zLibDll/minizip.html )",
            "",
            "contrib/minizip/ioapi.c\n"
            "\n"
            "\n"
            "contrib/minizip/ioapi.h\n"
            "\n"
            "\n"
            "contrib/minizip/iowin32.c\n"
            "\n"
            "\n"
            "contrib/minizip/iowin32.h\n"
            "\n"
            "\n"
            "contrib/minizip/miniunz.c\n"
            "\n"
            "\n"
            "contrib/minizip/minizip.c\n"
            "\n"
            "\n"
            "contrib/minizip/unzip.c\n"
            "\n"
            "\n"
            "contrib/minizip/unzip.h\n"
            "\n"
            "\n"
            "contrib/minizip/zip.c\n"
            "\n"
            "\n"
            "contrib/minizip/zip.h",
        ],
        ["Copyright (C) 1998-2005 Gilles Vollant", "", "contrib/minizip/crypt.h"],
        ["Copyright (C) 1998 by Andreas R. Kleinert", "", "amiga/Makefile.pup"],
        [
            "Copyright (C) 1998 - 2010 Gilles Vollant, Even Rouault, Mathias Svensson",
            "",
            "contrib/minizip/unzip.c",
        ],
        ["Copyright (C) 1995-2017 Mark Adler", "", "inffast.c\n\n\ninftrees.c"],
        ["Copyright (C) 1995-2017 Jean-loup Gailly, Mark Adler", "", "Makefile.in"],
        [
            "Copyright (C) 1995-2017 Jean-loup Gailly and Mark Adler",
            "",
            "deflate.c\n\n\nzlib.3\n\n\nzlib.3.pdf/zlib.3\n\n\nzlib.h",
        ],
        ["Copyright (C) 1995-2017 Jean-loup Gailly", "", "trees.c\n\n\nzutil.c"],
        ["Copyright (C) 1995-2017 Jean-Loup Gailly, Mark Adler", "", "os400/make.sh"],
        [
            "Copyright (C) 1995-2016 Mark Adler",
            "",
            "infback.c\n\n\ninflate.c\n\n\ninflate.h",
        ],
        [
            "Copyright (C) 1995-2016 Jean-loup Gailly, Mark Adler",
            "",
            "zconf.h\n\n\nzconf.h.cmakein\n\n\nzconf.h.in\n\n\nzutil.h",
        ],
        ["Copyright (C) 1995-2016 Jean-loup Gailly", "", "deflate.h"],
        ["Copyright (C) 1995-2011, 2016 Mark Adler", "", "adler32.c"],
        ["Copyright (C) 1995-2006, 2011, 2016 Jean-loup Gailly", "", "test/example.c"],
        [
            "Copyright (C) 1995-2006, 2010, 2011, 2016 Jean-loup Gailly",
            "",
            "test/minigzip.c",
        ],
        ["Copyright (C) 1995-2006, 2010, 2011, 2012, 2016 Mark Adler", "", "crc32.c"],
        [
            "Copyright (C) 1995-2005, 2014, 2016 Jean-loup Gailly, Mark Adler",
            "",
            "compress.c",
        ],
        ["Copyright (C) 1995-2005, 2010 Mark Adler", "", "inftrees.h"],
        [
            "Copyright (C) 1995-2003, 2010, 2014, 2016 Jean-loup Gailly, Mark Adler",
            "",
            "uncompr.c",
        ],
        ["Copyright (C) 1995-2003, 2010 Mark Adler", "", "inffast.h"],
        [
            "Copyright (C) 1995-1998 Jean-loup Gailly.",
            "",
            "msdos/Makefile.dj2\n\n\nmsdos/Makefile.emx\n\n\nold/Makefile.emx",
        ],
        ["(C) 1995-2017 Jean-loup Gailly and Mark Adler", "", "README"],
    ]

    assert tables["copyrights-user-findings"]["ROWS"] == [["", "", ""]]
    assert tables["bulk-findings"]["ROWS"] == [
        [
            "[remove] Zlib-possibility, [add] Zlib",
            "For conditions of distribution and use, see copyright notice in zlib.h",
            "Makefile.in\n"
            "\n"
            "\n"
            "adler32.c\n"
            "\n"
            "\n"
            "compress.c\n"
            "\n"
            "\n"
            "crc32.c\n"
            "\n"
            "\n"
            "deflate.c\n"
            "\n"
            "\n"
            "deflate.h\n"
            "\n"
            "\n"
            "examples/gun.c\n"
            "\n"
            "\n"
            "examples/zran.c\n"
            "\n"
            "\n"
            "gzclose.c\n"
            "\n"
            "\n"
            "gzguts.h\n"
            "\n"
            "\n"
            "gzlib.c\n"
            "\n"
            "\n"
            "gzread.c\n"
            "\n"
            "\n"
            "gzwrite.c\n"
            "\n"
            "\n"
            "infback.c\n"
            "\n"
            "\n"
            "inffast.c\n"
            "\n"
            "\n"
            "inffast.h\n"
            "\n"
            "\n"
            "inflate.c\n"
            "\n"
            "\n"
            "inflate.h\n"
            "\n"
            "\n"
            "inftrees.c\n"
            "\n"
            "\n"
            "inftrees.h\n"
            "\n"
            "\n"
            "msdos/Makefile.dj2\n"
            "\n"
            "\n"
            "msdos/Makefile.emx\n"
            "\n"
            "\n"
            "old/Makefile.emx\n"
            "\n"
            "\n"
            "old/os2/Makefile.os2\n"
            "\n"
            "\n"
            "test/example.c\n"
            "\n"
            "\n"
            "test/infcover.c\n"
            "\n"
            "\n"
            "test/minigzip.c\n"
            "\n"
            "\n"
            "trees.c\n"
            "\n"
            "\n"
            "uncompr.c\n"
            "\n"
            "\n"
            "zconf.h\n"
            "\n"
            "\n"
            "zconf.h.cmakein\n"
            "\n"
            "\n"
            "zconf.h.in\n"
            "\n"
            "\n"
            "zutil.c\n"
            "\n"
            "\n"
            "zutil.h",
        ],
        [
            "[add] Public-domain",
            "Not copyrighted -- provided to the public domain",
            "examples/fitblk.c\n\n\nexamples/zlib_how.html\n\n\nexamples/zpipe.c",
        ],
    ]

    assert tables["non-functional-licenses"]["ROWS"] == []
    assert tables["irrelevant-files"]["ROWS"] == [
        ["debian/patches", "use-dso", "No license found"],
        [".", "INDEX", "Perl-possibility"],
        ["contrib/minizip", "MiniZip64_info.txt", "Zlib"],
        [".", "FAQ", "GPL"],
        ["zlib.3.pdf", "zlib.3", "UnclassifiedLicense\n\n\nZlib"],
        [".", "zlib.3", "Zlib"],
    ]

    assert tables["comment-for-irrelevant-files"]["ROWS"] == [["", "", ""]]
    assert tables["do-not-use-files"]["ROWS"] == []
    assert tables["comment-for-do-not-use-files"]["ROWS"] == []
    assert tables["clearing-protocol-change-log"]["ROWS"] == [
        ["Last Update", "Responsible", "Comments"],
        ["", "", ""],
    ]
