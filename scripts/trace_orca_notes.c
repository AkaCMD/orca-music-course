#include "field.h"
#include "gbuffer.h"
#include "sim.h"
#include "vmio.h"
int main(int argc,char **argv){
  if(argc<2||argc>3)return 1;
  Usz limit=argc==3?(Usz)strtoul(argv[2],NULL,10):32;
  Field f;field_init(&f);
  if(field_load_file(argv[1],&f)!=Field_load_error_ok)return 2;
  Mbuf_reusable m;mbuf_reusable_init(&m);mbuf_reusable_ensure_size(&m,f.height,f.width);
  Oevent_list events;oevent_list_init(&events);
  for(Usz tick=0;tick<limit;tick++){
    mbuffer_clear(m.buffer,f.height,f.width);oevent_list_clear(&events);
    orca_run(f.buffer,m.buffer,f.height,f.width,tick,&events,0);
    for(Usz j=0;j<events.count;j++){
      Oevent *e=events.buffer+j;
      if(e->any.oevent_type==Oevent_type_midi_note){
        Oevent_midi_note *n=&e->midi_note;
        printf("%zu %u %u %u %u\n",tick,n->octave*12+n->note,n->channel,n->velocity,n->duration);
      }
    }
  }
  oevent_list_deinit(&events);mbuf_reusable_deinit(&m);field_deinit(&f);
  return 0;
}
