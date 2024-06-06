/*

    File: partxboxn.c

    Copyright (C) 1998-2009 Christophe GRENIER <grenier@cgsecurity.org>
  
    This software is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
  
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
  
    You should have received a copy of the GNU General Public License along
    with this program; if not, write the Free Software Foundation, Inc., 51
    Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

 */


#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#if defined(DISABLED_FOR_FRAMAC)
#undef HAVE_NCURSES
#endif

#if defined(HAVE_NCURSES)
#include <stdio.h>
#ifdef HAVE_STDLIB_H
#include <stdlib.h>
#endif
#include "types.h"
#include "common.h"
#include "fnctdsk.h"
#include "intrf.h"
#include "intrfn.h"
#include "chgtypen.h"
#include "partxboxn.h"

extern const arch_fnct_t arch_xbox;

list_part_t *add_partition_xbox_ncurses(disk_t *disk_car, list_part_t *list_part)
{
  int position=0;
  int done = FALSE;
  partition_t *new_partition=partition_new(&arch_xbox);
  new_partition->part_offset=disk_car->sector_size;
  new_partition->part_size=disk_car->disk_size-disk_car->sector_size;
  while (done==FALSE)
  {
    int command;
    static const struct MenuItem menuGeometry[]=
    {
      { 's', "Sector", 	"Change starting sector" },
      { 'S', "Sector", 	"Change ending sector" },
      { 'T' ,"Type",	"Change partition type"},
      { 'd', "Done", "" },
      { 0, NULL, NULL }
    };
    aff_copy(stdscr);
    wmove(stdscr,4,0);
    wprintw(stdscr,"%s",disk_car->description(disk_car));
    wmove(stdscr,10, 0);
    wclrtoeol(stdscr);
    aff_part(stdscr, AFF_PART_BASE, disk_car, new_partition);
    wmove(stdscr,INTER_GEOM_Y, INTER_GEOM_X);
    wclrtoeol(stdscr);
    wrefresh(stdscr);
    command=wmenuSimple(stdscr,menuGeometry, position);
    switch (command) {
      case 's':
	{
	  uint64_t part_offset;
	  part_offset=new_partition->part_offset;
	  wmove(stdscr, INTER_GEOM_Y, INTER_GEOM_X);
	  new_partition->part_offset=(uint64_t)ask_number(
	      new_partition->part_offset/disk_car->sector_size,
	      0x800/disk_car->sector_size,
	      (disk_car->disk_size-1)/disk_car->sector_size,
	      "Enter the starting sector ") *
	    (uint64_t)disk_car->sector_size;
	  new_partition->part_size=new_partition->part_size + part_offset - new_partition->part_offset;
	  position=1;
	}
	break;
      case 'S':
	wmove(stdscr, INTER_GEOM_Y, INTER_GEOM_X);
	new_partition->part_size=(uint64_t)ask_number(
	      (new_partition->part_offset+new_partition->part_size-1)/disk_car->sector_size,
	      new_partition->part_offset/disk_car->sector_size,
	      (disk_car->disk_size-1)/disk_car->sector_size,
	      "Enter the ending sector ") *
	  (uint64_t)disk_car->sector_size +
	  disk_car->sector_size - new_partition->part_offset;
	position=2;
	break;
      case 'T':
      case 't':
	change_part_type_ncurses(disk_car, new_partition);
	position=3;
	break;
      case key_ESC:
      case 'd':
      case 'D':
      case 'q':
      case 'Q':
	done = TRUE;
	break;
    }
  }
  if(new_partition->part_size>0 && new_partition->part_type_xbox>0)
  {
    int insert_error=0;
    list_part_t *new_list_part=insert_new_partition(list_part, new_partition, 0, &insert_error);
    if(insert_error>0)
    {
      free(new_partition);
      return new_list_part;
    }
    new_partition->status=STATUS_PRIM;
    if(arch_xbox.test_structure(list_part)!=0)
      new_partition->status=STATUS_DELETED;
    return new_list_part;
  }
  free(new_partition);
  return list_part;
}
#endif
