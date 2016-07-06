{% from "salt-junit-output/map.jinja" import salt_junit_output with context %}

/{{ salt_junit_output.extmod_dir }}/output/junit.py:
  file.managed:
    - source: salt://salt-junit-output/files/junit.py
    - makedirs: True

{% if salt_junit_output.add_extmode_config %}
/etc/salt/master.d/99-extension_modules.conf:
  file.managed:
    - source: salt://salt-junit-output/files/99-extension_modules.conf
    - template: jinja
    - defaults:
        extmode_dir: {{ salt_junit_output.extmod_dir }}

salt_junit_output_salt-master:
  service.running:
    - name: salt-master
    - watch:
      - file: /etc/salt/master.d/99-extension_modules.conf
{% endif %}
